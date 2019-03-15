import configparser
import os
import sys
import argparse

def args_parser():
    parser = argparse.ArgumentParser(description='Script launcher and manager.', add_help=True)
    parser.add_argument('--config', "-c", metavar="FILE", help='fsman configuration file location')

    args = parser.parse_args()
    return vars(args)

cfg = args_parser().get("config")
if cfg is None:
    CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), "fsman.cfg")
else:
    CONFIG = os.path.realpath(cfg)
    #sys.stdout.write("cfg: "+str(os.path.realpath(cfg)))
    #sys.stdout.write("cfg: "+str(os.path.realpath(cfg)))

default_config = {
        'Provider': {
            'provider_type': 'glob',
            'glob' : "tests/*py",
            'script' : "provider"
            },
        'Output': {
            'status': 'status.json',
            'output_dir': "output/"
            },
        'FXECUTOR':{
            'executor_path' : 'python'
            },
        'GUI':{
            'indicator_text': '~>'
            }
        }

REL_PATH = ["script", "status", "output_dir"]

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
                val = config.get(section, key).strip("'").strip('"')
                #sys.stdout.write(f'{val} ')
                if key in REL_PATH:
                    if os.path.abspath(val):
                        val = os.path.join(os.path.dirname(CONFIG), val)
                        #sys.stdout.write(f'{val} ')
                #sys.stdout.write(str(val))
                return val

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
    config = configread()

    if not os.path.exists(CONFIG):
        open(CONFIG, 'a').write("")

    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)
    with open(CONFIG, 'w') as configfile:
        config.write(configfile)

