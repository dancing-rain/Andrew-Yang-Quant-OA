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
    
def GetBasicInfo():
    to_return = "Username: " + user_info.name + "\n"
    to_return += "Cake Day: " + user_info.cake_day + "\n"
    to_return += "User Age: " + str(user_info.age) + "\n"
    to_return += "User Comment Karma: " + str(user_info.karma_comments) + "\n"
    to_return += "User Overall Karma: " + str(user_info.karma_overall) + "\n"
    to_return += "User is a moderator: " + str(user_info.moderator) + "\n"
    to_return += "User is suspended: " + str(user_info.suspended) + "\n"
    to_return += "User ID: " + user_info.id + "\n"
    return to_return
    
def FindFiveMostVotedSubmissions():
    to_return = "\nTop 5 most upvoted posts (Out of last 99 posts):\n"
    sorted_submissions = sorted(user_submissions_list,key=lambda x:x.score, reverse=True)
    idx = 0
    for submission in sorted_submissions:
        if idx < 5 and idx < len(sorted_submissions):
            to_return += str(idx + 1) + ")\t" + "score: " + str(submission.score) + " | " + datetime.utcfromtimestamp(int(submission.created_utc)).strftime("%m/%d/%Y, %H:%M:%S") + "UTC | " + str(submission.num_comments) + " comments | Title: " + submission.title + "\n"
            #appends in the following format: POST_NUMBER)      score: UPVOTE_SCORE | DATE_TIME_UTC | COMMENT_COUNT comments | Title: TITLE
        elif idx < 5 and idx == len(sorted_submissions) - 1:
            to_return += "X)\tUser has made < 6 total submissions\n"
            #prints when user's total submission count is less than or equal to 5
        idx+=1
    return to_return;
        
def FindFiveMostVotedComments():
    to_return = "\nTop 5 most upvoted comments (Out of last 99 posts):\n"
    sorted_comments = sorted(user_comments_list,key=lambda x:x.score, reverse=True)
    idx = 0
    for comments in sorted_comments:
        if idx < 5 and idx < len(sorted_comments):
            comment_body = comments.body.replace("\n","")
            if len(comment_body) > 40:
                comment_body = comment_body[0:100] + "..."
            to_return += str(idx + 1) + ")\t" + "score: " + str(comments.score) + " | " + datetime.utcfromtimestamp(int(comments.created_utc)).strftime("%m/%d/%Y, %H:%M:%S") + "UTC | " + str(len(comments.replies)) + " replies | contents: " + comment_body + "\n"
        elif idx < 5 and idx == len(sorted_comments) - 1:
            to_return += "X)\tUser has made < 6 total comments\n"
            #prints when user's total comment count is less than or equal to 5
        idx+=1
    return to_return
    
def FindVoteDistribution(): 
    to_return = "\nUser's top subreddits ranked by comment/submission upvotes (Out of last 198 interactions):\n"
    active_subreddits_map = {}
    #combine comments and submissions into dictionary format {sub name, upvote count} to easily organize subreddits and increment their upvote counts
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
    #convert map back to list, then use built-in triple parameter sort method to sort subreddits by upvote count
    active_subreddits_list = []
    for i,(k, v) in enumerate(active_subreddits_map.items()):
        active_subreddits_list.append([k, v])
    descending_subreddit_by_activity = sorted(active_subreddits_list,key=lambda x:x[1], reverse=True)
    idx = 0
    #print subreddit upvote distribution in descending order
    for subreddit in descending_subreddit_by_activity:
        to_return += str(idx+1) + ")\tSubreddit: " + subreddit[0] + " | " + str(subreddit[1]) + " vote(s)\n"
        idx+=1
    return to_return
    
def FindMostActive():
    to_return = "\nTop active subreddits ranked by quantity of comments and submissions (Out of last 198 interactions):\n"
    active_subreddits_map = {}
    #combine comments and submissions into dictionary format {sub name, upvote count} to easily organize subreddits and increment their interaction count
    for comments in user_comments_list:
        sub_name = comments.subreddit.display_name
        if sub_name in active_subreddits_map.keys():
            active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + 1
        else:
            active_subreddits_map[sub_name] = 1
    for submissions in user_submissions_list:
        sub_name = submissions.subreddit.display_name
        if sub_name in active_subreddits_map.keys():
            active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + 1
        else:
            active_subreddits_map[sub_name] = 1
    #convert map back to list, then use built-in triple parameter sort method to sort subreddits by upvote count
    active_subreddits_list = []
    for i,(k, v) in enumerate(active_subreddits_map.items()):
        active_subreddits_list.append([k, v])
    descending_subreddit_by_activity = sorted(active_subreddits_list,key=lambda x:x[1], reverse=True)
    idx = 0
    #print subreddit interactions in descending order
    for subreddit in descending_subreddit_by_activity:
        to_return += str(idx+1) + ")\tSubreddit: " + subreddit[0] + " | " + str(subreddit[1]) + " interaction(s)\n"
        idx+=1
    return to_return

class UserInfo:
    id: str #user's id - short series of alphanumeric charaacters
    name: str #user's name
    cake_day: str #month/day/year
    age: int #in days
    karma_comments: int #comment karma, may be slightly off
    karma_overall: int #comment karma + post karma, may be slightly off
    moderator: bool #user is a subreddit moderator
    suspended: bool #user is suspended from reddit
    five_most_voted_submissions: str
    five_most_voted_comments: str
    vote_distribution: str
    most_active_subs: str
    
    def __init__(self, id="", name="", cake_day="", age=0, karma_comments=0, karma_overall=0, moderator=False, suspended=False):
        self.id = id
        self.name = name
        self.cake_day = cake_day
        self.age = age
        self.karma_comments = karma_comments
        self.karma_overall = karma_overall
        self.moderator = moderator
        self.suspended = suspended
        
'''class TopFiveVotedSubmissionsData:
    descriptive_header: str
    
    def __init__(self, descriptive_header="\nTop 5 most upvoted posts (Out of last 99 posts):\n"):
        self.descriptive_header = descriptive_header
class TopFiveVotedCommentsData:
    descriptive_header: str
    def __init__(self, descriptive_header="\nTop 5 most upvoted comments (Out of last 99 posts):\n"):
        self.descriptive_header = descriptive_header
class VoteDistribution:
    descriptive_header: str
    def __init__(self, descriptive_header="\nTop active subreddits ranked by quantity of comments and submissions (Out of last 198 interactions):\n"):
        self.descriptive_header = descriptive_header
class MostActiveSubs:
    descriptive_header: str
    def __init__(self, descriptive_header="\nTop active subreddits ranked by quantity of comments and submissions (Out of last 198 interactions):\n"):
        self.descriptive_header = descriptive_header'''

if __name__ == '__main__':
    print()
    user_name = GetUsernameInput()
    print()
    
    user_as_redditor = reddit.redditor(user_name)
    user_info = UserInfo()
    
    user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
    user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
    
    if user_shadowbanned:
        print("User is shadowbanned - only contains name and is_suspended attributes")
    else:
        SetBasicInfo()
        print(GetBasicInfo())
        
        print(FindFiveMostVotedSubmissions())
        print(FindFiveMostVotedComments())
        
        user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
        user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
        print(FindVoteDistribution())
        
        user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
        user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
        print(FindMostActive())
    print("")