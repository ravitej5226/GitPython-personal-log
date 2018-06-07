import config
from datetime import date, timedelta

class CommitFetcher:
    def __init__(self,repo):
        self.required_commits_=[]
        self.config=config.get_config_file()
        self.repo=repo
    
    def get_commits(self):
        return self.required_commits_
    
    def get_committers(self):
        c=self.repo.iter_commits()
        committers=[]        
        index=1
        for x in c:
            if(not x.author.name in committers):                
                committers.append(x.author.name)        
                index=index+1
            
            if(index>15):
                break
            
        return committers

class LastCommitFetcher(CommitFetcher):
    def get_commits(self):        
        """ Gets the commits of the user that needs to be logged """
        commits = self.repo.iter_commits()       
        user = self.config['source_repo']['committer']
        for commit in commits:
            # Get user's commit and make sure it is not a MERGE commit
            if(commit.author.name == user and len(commit.parents) == 1):
                self.required_commits_.append(commit)
                break

        return self.required_commits_        

class CurrentDayCommitFetcher(CommitFetcher):
    def get_commits(self):
        commits = self.repo.iter_commits()       
        user = self.config['source_repo']['committer']
        for commit in commits:
            # Get user's commit and make sure it is not a MERGE commit
            if(commit.author.name == user and len(commit.parents) == 1 and commit.committed_datetime.date()==date.today()):
                print(commit)
                self.required_commits_.append(commit)
                break

        return self.required_commits_        
        