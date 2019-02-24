from glob import glob
import configurer as config
import sys

def get_paths():
    provider_type = config.get("provider_type")
    if provider_type == "glob":
        program_paths = glob(config.get("glob"))
    elif provider_type == "script":
        program_paths = config.get("script")
    return program_paths
