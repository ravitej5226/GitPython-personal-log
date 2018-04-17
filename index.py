""" Script that gets the required commits from the source repository
    and logs it into the log file in another repository
"""
from __future__ import print_function
import sys
import argparse
import datetime
import openpyxl
import config
from git import Repo
from termcolor import cprint
from colorama import init
from commit_fetcher import *

CONFIG = config.get_config_file()

# initialize colored text on terminal
init()

COLORS = {'success': 'green', 'error': 'red',
          'warning': 'magenta', 'information': 'cyan'}


def get_source_repo():
    """ Loads and returns the source repository """
    return Repo(CONFIG['source_repo']['local_path'])

def get_formatted_file_list(commit):
    """ Formats and returns the file list in a given commit """
    file_list = commit.stats.files.keys()
    return ['\\{0}'.format(f.replace('/', '\\')) for f in file_list]


def get_log_repo():
    """ Loads and returns the log repository """
    return Repo(CONFIG['log_repo']['local_path'])


def update_log_file(commits):
    """ Updates the log file with the given commit information and saves the file
        Returns true if operation is successful else returns false
    """
    # Open workbook and sheet
    workbook = openpyxl.load_workbook(CONFIG['log_repo']['log_xl_file_path'])
    sheet = workbook[CONFIG['log_repo']['xl_sheet_name']]
    last_row = None

    # Get the last non-empty row so we can add in the next empty row
    for row in sheet.rows:
        values = [cell.value for cell in row]
        if not any(values):
            last_row = row[0].row - 1
            print("last row with data is {0}".format(row[0].row - 1))
            break

    # Get values for all the fields in the sheet
    current_row = last_row + 1
    date = '{dt.month}/{dt.day}/{dt.year}'.format(dt=datetime.datetime.now())
    author = CONFIG['log_repo']['author']

    for commit in commits:
        sheet['A' + str(current_row)] = current_row - 1
        sheet['B' + str(current_row)] = date
        sheet['C' + str(current_row)] = ('\n'.join(get_formatted_file_list(commit))).strip('\n')        
        sheet['D' + str(current_row)] = commit.repo.active_branch.name
        sheet['E' + str(current_row)] = author
        sheet['F' + str(current_row)] = commit.message.strip('\n')
        sheet['G' + str(current_row)] = 'NO'
        current_row = current_row + 1
    workbook.save(CONFIG['log_repo']['log_xl_file_path'])
    return True


def log_commits_to_file(commit_fetcher):
    """ Gets all the commits from the source repository and
    logs in an Excel sheet in the log repository    
    """
    try:

        # Read the source repository
        cprint('Getting the latest version of the source repository',
               COLORS['information'])
        source_repo = get_source_repo()
        data = source_repo.remotes[0].pull()
        cprint('Fetching the source repository successful', COLORS['success'])

        # Check for is dirty
        if(source_repo.is_dirty()):
            cprint('Source repository has some uncommitted changes',
                   COLORS['warning'])

        # Get the required commit
        cprint('Getting the user commits', COLORS['information'])
        user_commits = commit_fetcher.get_commits()

        cprint('Getting the latest version of the log repository',
               COLORS['information'])
        # Load the log repository
        log_repo = get_log_repo()

        # Git pull the log repository
        log_repo.remotes[0].pull()

        # Check for is dirty
        if(log_repo.is_dirty()):
            cprint(
                'ERROR: Log repository has some uncommitted changes.'\
                'Please revert or commit before proceeding further.', COLORS['error'])
            cprint('Exiting the program now...', COLORS['error'])
            quit()

        # Update the excel sheet
        cprint('Updating the log file', COLORS['information'])
        status = update_log_file(user_commits)

        if(not status):
            cprint('There was an error updating the log file. Please contact the administrator','red')        
            quit()

        # Git commit and push
        cprint('Committing the log file...', COLORS['information'])
       # log_repo.index.add([CONFIG['log_repo']['log_xl_file_path']])
       # log_repo.index.commit('Updated')

        cprint('Pushing the log file', COLORS['information'])
        # log_repo.remotes[0].push()
        cprint('Updating the log file successful', COLORS['success'])
    except Exception as e:
        cprint('ERROR:\n{0}\nExiting the program now...'.format(
            str(e)), COLORS['error'])



def handle_user_options(args):
    if(args.setup):
        print('setup')
    elif(args.today):               
        repo=get_source_repo()
        commit_fetcher=CurrentDayCommitFetcher(repo)
        log_commits_to_file(commit_fetcher)
    else:
        repo=get_source_repo()
        commit_fetcher=LastCommitFetcher(repo)
        log_commits_to_file(commit_fetcher)
       
        print('latest')


if __name__ == "__main__":
    #log_commits_to_file()
    parser = argparse.ArgumentParser(description='Process some integers.')
    group=parser.add_mutually_exclusive_group()
    group.add_argument('--setup','-s',help='Sets up the script for the user by initializing all the required information',action='store_true')
    group.add_argument('--latest','-l',help='Logs the last commit to the log file',action='store_true',dest='latest')
    group.add_argument('--today','-t',help='Logs all the commits of today to the log file',action='store_true')    
    group.add_argument('--version','-v',help='Displays the version of the script',action='version',version='1.0')
    
    args=parser.parse_args()
    handle_user_options(args)
    
    
