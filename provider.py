from glob import glob

#todo: fetch pattern from cfg
program_paths = glob('tests/*py')
#program_paths = glob('keeper/test_scripts/*')

def glob():
    return program_paths

