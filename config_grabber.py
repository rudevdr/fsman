from string import ascii_lowercase
import re

class Config_Grabber():
    def config_grabber(self, key):
        config_invalid = open(self.config_name).read().strip().split('\n')
        config_valid = [line for line in config_invalid if line.startswith(tuple(ascii_lowercase))]
        config_element = [element for element in config_valid if element.startswith(key)][0]
        config_value_invalid = config_element[config_element.find('=')+1:]
        try:
            first_occurrance_of = re.findall(r'\d|\'|"|\\', config_value_invalid)[0]
            if first_occurrance_of is '\\':
                try:
                    search_from = config_invalid.index(config_element)+1
                    start = search_from+[i for i, n in enumerate(config_invalid[search_from:]) if n == '"""'][0]
                    end = search_from+[i for i, n in enumerate(config_invalid[search_from:]) if n == '"""'][1]+1
                    required_list = config_invalid[start:end]
                    result = '\n'.join(required_list[1:-1])
                    return result
                except:
                    print(key+' <= Unacceptable format! Please put desired format between \\""""%FORMAT%""')
            elif first_occurrance_of.isdigit():
                return re.findall(r'\d+', config_value_invalid)[0]
            elif first_occurrance_of.startswith(('"', "'")):
                try:
                    return re.findall(r'"(.*?)"', config_value_invalid)[0]
                except:
                    print(key+" <= put its value in DOUBLE QUOTATION MARK!(\"\") in config!!")

        except IndexError:
            print(key+" <= value is not set in config!!!")

    def __init__(self):
        self.config_name = "fsman.cfg"
