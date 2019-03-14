from glob import glob
import configurer as config
import sys

def get_paths():
    provider_type = config.get("provider_type")
    if provider_type == "glob":
        program_paths = glob(config.get("glob"))
    elif provider_type == "script":
        provider_script = config.get("script")

        import importlib.util #https://stackoverflow.com/a/67692/6420136
        spec = importlib.util.spec_from_file_location("*", provider_script)
        foo = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(foo)
        except FileNotFoundError:
            return [f"[Invalid provider script {provider_script}!", "Please make sure the path is correct.]"]

        program_paths = foo.main()
    return program_paths
