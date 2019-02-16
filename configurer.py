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

    if item in add_keys_default():
        #TODO: if key not found in config, then check if key is in default dictionary. if it is then add to file and return the default value, else raise error
        add_default(key, value)
        return default
    else:
        raise KeyError(f'Setting for "{item}" is not found in {CONFIG}')


def all_keys_default():
    '''
    yields a tuple of key, value of all dict inside dict (secondary dicts)
    '''
    #TODO: see doc

    for k, v in d.items():
        for key, value in v.items():
            yield key, value

def add_default(key, value):
    '''
    writes key, value to CONFIG file
    '''

    #TODO: see doc
