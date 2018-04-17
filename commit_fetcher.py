import config
from datetime import date, timedelta

class CommitFetcher:
    def __init__(self,repo):
        self.required_commits_=[]
        self.config=config.get_config_file()
        self.repo=repo
    
    def get_commits(self):
        return self.required_commits_

class LastCommitFetcher(CommitFetcher):
    def get_commits(self):        
        """ Gets the commits of the user that needs to be logged """
        commits = self.repo.iter_commits()       
        user = self.config['source_repo']['use_value']
        for commit in commits:
            # Get user's commit and make sure it is not a MERGE commit
            if(commit.author.name == user and len(commit.parents) == 1):
                self.required_commits_.append(commit)
                break

        return self.required_commits_        

class CurrentDayCommitFetcher(CommitFetcher):
    def get_commits(self):
        commits = self.repo.iter_commits()       
        user = self.config['source_repo']['use_value']
        for commit in commits:
            # Get user's commit and make sure it is not a MERGE commit
            if(commit.author.name == user and len(commit.parents) == 1 and commit.committed_datetime.date()==date.today()):
                print(commit)
                self.required_commits_.append(commit)
                break

        return self.required_commits_        
        