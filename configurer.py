import configparser

CONFIG = "fsman.cfg"

default_config = {
    'Provider': {
        'source_file': 'glob',
        'glob' : "*/*",
    }
}


def configread():
    config = configparser.ConfigParser()
    config.read(CONFIG)

    return config


def all_keys():
    config = configread()

    for section in config.sections():
        for key in config.options(str(section)):
            yield key


def get(item):
    config = configread()

    for section in config.sections():
        for key in config.options(str(section)):
            if item == key:
                return config.get(section, key).strip("'").strip('"')

    for section, key, value in iter(all_keys_default()):
        if item == key:
            add_config(section, key, value)
            return value

    raise KeyError(f'Setting for "{item}" is not found in {CONFIG}')


def all_keys_default():
    '''
    yields a tuple of key, value of all dict inside dict (secondary dicts)
    '''

    for k, v in default_config.items():
        for key, value in v.items():
            yield (k, key, value)

def add_config(section, key, value):
    '''
    writes key, value to CONFIG file
    '''
    #config_read = configread()
    #config = configparser.ConfigParser()
    config = configread()

    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)
