""" Contains all the methods and variables that operate on the config file"""

import yaml

def get_config_file():
    '''
    Returns the configuration file
    Convert the yaml into a dictionary
    '''
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)

    return config
