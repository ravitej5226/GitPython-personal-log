""" Contains all the methods and variables that operate on the config file"""

import yaml
from commit_fetcher import *


def get_config_file():
    '''
    Returns the configuration file
    Convert the yaml into a dictionary
    '''
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)

    return config

def setup_config(repo):
    print('Setting up... Please enter following information to complete setup')
    print('Press Enter key to retain the defaults')
    config =get_config_file()

    # Get the source repo local location
    source_repo_local_path=raw_input('Enter the source repo local path ({0}):'.format(config['source_repo']['local_path']))
    if(source_repo_local_path.strip()!=''):
        config['source_repo']['local_path']=source_repo_local_path.strip()
    
    # Get the committer name
    committer=raw_input('Enter the name of the committer ({0}) [Enter "find" to know your name in the GIT repo]:'.format(config['source_repo']['committer']))
    
    if(committer.strip()=='find'):
        # Get the committer names
        commit_fetcher=CommitFetcher(repo)
        committers=set(commit_fetcher.get_committers())
        index=1
        for user in committers:
            print('{0}. {1}'.format(index,user))
            index=index+1
        isSet=False
        while(not isSet):
            user_choice=raw_input('Enter the index number of the committer from above list set')
            user_choice=user_choice.rstrip()
            # Validate user choice
            # Validate integer
            # Validate range
            if(not (user_choice.isdigit() and int(user_choice)<index)):
                print('Invalid input!')
            else:
                isSet=True
                config['source_repo']['committer']=list(committers)[int(user_choice)-1]

            
    elif(committer.strip()!=''):
        config['source_repo']['committer']=committer.strip()

    # Get the log repo local location
    log_repo_local_path=raw_input('Enter the log repo local path ({0}):'.format(config['log_repo']['local_path']))

    if(log_repo_local_path.strip()!=''):
        config['log_repo']['local_path']=log_repo_local_path.strip()
    
    # Get the sheet name    
    log_file_sheet=raw_input('Enter the log file sheet name ({0}):'.format(config['log_repo']['xl_sheet_name']))

    if(log_file_sheet.strip()!=''):
        config['log_repo']['xl_sheet_name']=log_file_sheet.strip()
    
    # Get the author name
    author=raw_input('Enter the author name to be associated to the commits ({0}):'.format(config['log_repo']['author']))
    if(author.strip()!=''):
        config['log_repo']['author']=author.strip()


    with open('config.yml', 'w') as config_file:
        yaml.dump(config,config_file,default_flow_style=False)
    
    