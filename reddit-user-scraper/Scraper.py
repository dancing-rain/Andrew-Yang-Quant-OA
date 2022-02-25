#Dependencies
from statistics import mode
from unicodedata import name
import praw
import os
from datetime import datetime
import time
from prawcore.exceptions import NotFound


abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
os.chdir(dir_name)

user_info = None;
user_as_redditor = None;
user_comments_list = None
user_submissions_list = None
user_shadowbanned = False;

reddit = praw.Reddit( #instance of praw reddit for API access
    client_id = 'g1newHxnqEdQYH8vN8hSLw',
    client_secret = '34WhZ0gJxY5bmnrd1OpPDocqMWV8Wg',
    password = 'Bestlangpython666',
    user_agent = 'andrew_web_scraper',
    username = 'Ok-General847',
)
reddit.read_only = True;

def UserExists(name: str): #Check if username exists
    try:
        reddit.redditor(name).id
    except NotFound:
        return False
    return True

def GetUsernameInput(): #Check if inputted username is valid
    name = input("Enter username (eg _dancingrain_): ")
    if (not UserExists(name)):
        print("\nUsername not found, try again\n")
        return GetUsernameInput()
    return name;

def GetDate():
    cake_day_date = datetime.utcfromtimestamp(int(user_as_redditor.created_utc)).strftime("%m/%d/%Y, %H:%M:%S")
    return cake_day_date
    
def GetAge():
    cake_day_unix = user_as_redditor.created_utc
    current_time_unix = time.time()
    seconds_per_day = 86400
    return int((current_time_unix-cake_day_unix)/seconds_per_day)

def SetBasicInfo():
    #Username
    user_info.name = user_as_redditor.name
    #Is user suspended
    user_info.suspended = True;
    try:
        user_as_redditor.is_suspended
    except AttributeError:
        user_info.suspended = False;
        user_shadowbanned = False;
    if not user_shadowbanned: 
        #ID
        user_info.id = user_as_redditor.id
        #UTC
        user_info.cake_day = GetDate() + " UTC"
        #Days
        user_info.age = str(GetAge()) + " days"
        #PRAW Karma may vary from actual
        user_info.karma_comments = str(user_as_redditor.comment_karma) + " karma"
        user_info.karma_overall = str(user_as_redditor.link_karma + user_as_redditor.comment_karma) + " karma"
        #Is user a moderator
        user_info.moderator = False;
        if (user_as_redditor.is_mod):
            user_info.moderator = True;
    
def PrintBasicInfo():
    print("Username: " + user_info.name)
    print("Cake Day: " + user_info.cake_day)
    print("User Age: " + str(user_info.age))
    print("User Comment Karma: " + str(user_info.karma_comments)) 
    print("User Overall Karma: " + str(user_info.karma_overall)) 
    print("User is a moderator: " + str(user_info.moderator))
    print("User is suspended: " + str(user_info.suspended))
    print("User ID: " + user_info.id)
    
def FindPrintFiveMostVotedSubmissions():
    print("\nTop 5 most upvoted posts (Out of last 99 posts):")
    sorted_submissions = sorted(user_submissions_list,key=lambda x:x.score, reverse=True)
    idx = 0
    for submission in sorted_submissions:
        if idx < 5 and idx < len(sorted_submissions):
            print(str(idx + 1) + ")\t" + "score: " + str(submission.score) + " | " + datetime.utcfromtimestamp(int(submission.created_utc)).strftime("%m/%d/%Y, %H:%M:%S") + "UTC | " + str(submission.num_comments) + " comments | Title: " + submission.title)
        elif idx < 5 and idx == len(sorted_submissions) - 1:
            print("X)\tUser has made < 5 total submissions")
        idx+=1
        
def FindPrintFiveMostVotedComments():
    print("\nTop 5 most upvoted comments (Out of last 99 posts):")
    sorted_comments = sorted(user_comments_list,key=lambda x:x.score, reverse=True)
    idx = 0
    for comments in sorted_comments:
        if idx < 5 and idx < len(sorted_comments):
            comment_body = comments.body
            if len(comment_body) > 40:
                comment_body = comment_body[0:100] + "..."
            print(str(idx + 1) + ")\t" + "score: " + str(comments.score) + " | " + datetime.utcfromtimestamp(int(comments.created_utc)).strftime("%m/%d/%Y, %H:%M:%S") + "UTC | " + str(len(comments.replies)) + " replies | contents: " + comment_body)
        elif idx < 5 and idx == len(sorted_comments) - 1:
            print("X)\tUser has made < 5 total comments")
        idx+=1
    
def FindPrintVoteDistribution(): 
    print("\nTop active subreddits ranked by comment/submission upvotes (Out of last 198 interactions):")
    active_subreddits_map = {}
    for comments in user_comments_list:
        sub_name = comments.subreddit.display_name
        upvote_qty = comments.score
        if sub_name in active_subreddits_map.keys():
            active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + upvote_qty
        else:
            active_subreddits_map[sub_name] = upvote_qty
    for submissions in user_submissions_list:
        sub_name = submissions.subreddit.display_name
        upvote_qty = submissions.score
        if sub_name in active_subreddits_map.keys():
            active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + upvote_qty
        else:
            active_subreddits_map[sub_name] = upvote_qty
    active_subreddits_list = []
    for i,(k, v) in enumerate(active_subreddits_map.items()):
        active_subreddits_list.append([k, v])
    descending_subreddit_by_activity = sorted(active_subreddits_list,key=lambda x:x[1], reverse=True)
    idx = 0
    for subreddit in descending_subreddit_by_activity:
        print(str(idx+1) + ")\tSubreddit: " + subreddit[0] + " | " + str(subreddit[1]) + " votes")
        idx+=1
    
    

class User:
    id: str
    name: str
    cake_day: str #month/day/year
    age: int #in days
    karma_comments: int
    karma_overall: int
    moderator: bool
    suspended: bool
    
    def __init__(self, id="", name="", cake_day="", age=0, karma_comments=0, karma_overall=0, moderator=False, suspended=False):
        self.id = id
        self.name = name
        self.cake_day = cake_day
        self.age = age
        self.karma_comments = karma_comments
        self.karma_overall = karma_overall
        self.moderator = moderator
        self.suspended = suspended

if __name__ == '__main__':
    print("")
    user_name = GetUsernameInput()
    print("")
    
    user_as_redditor = reddit.redditor(user_name)
    user_info = User()
    
    user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
    user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
    
    if user_shadowbanned:
        print("User is shadowbanned - only contains name and is_suspended attributes")
    else:
        '''SetBasicInfo()
        PrintBasicInfo()
        
        FindPrintFiveMostVotedSubmissions()
        FindPrintFiveMostVotedComments()
        
        FindPrintVoteDistribution()'''
    print("")