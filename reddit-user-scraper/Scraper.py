#Dependencies
from array import array
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
file_name = "scraper_output.txt"
opened_file = open(file_name,"w")

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
        to_return += str(idx+1) + ")\t" + "r/" + subreddit[0] + " | " + str(subreddit[1]) + " vote(s)\n"
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
        to_return += str(idx+1) + ")\t" + "r/" + subreddit[0] + " | " + str(subreddit[1]) + " interaction(s)\n"
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
    info_keys: list
    info_values: list
    txt_delimiter: str
    
    def __init__(self, id="", name="", cake_day="", age=0, karma_comments=0, karma_overall=0, moderator=False, suspended=False, txt_delimiter = "UserInfo_delim"):
        self.id = id
        self.name = name
        self.cake_day = cake_day
        self.age = age
        self.karma_comments = karma_comments
        self.karma_overall = karma_overall
        self.moderator = moderator
        self.suspended = suspended
        self.info_keys = ["Username: ", "Cake Day: ", "Age: ", "User Comment Karma: ", "User Overall Karma: ", "User is a moderator: ", "User is suspended: ", "User ID: "] 
        self.info_values = [name, cake_day, age, karma_comments, karma_overall, moderator, suspended, id]
        self.txt_delimiter = txt_delimiter
    
    def SetBasicInfo(self):
        #Username
        self.name = user_as_redditor.name
        #Is user suspended
        self.suspended = True;
        try:
            self.user_as_redditor.is_suspended
        except AttributeError:
            self.suspended = False;
            user_shadowbanned = False;
        if not user_shadowbanned: 
            #ID
            self.id = user_as_redditor.id
            #UTC
            self.cake_day = datetime.utcfromtimestamp(int(user_as_redditor.created_utc)).strftime("%m/%d/%Y, %H:%M:%S") + " UTC"
            #Days
            self.age = str(int((time.time()-user_as_redditor.created_utc)/86400)) + " days"
            #PRAW Karma may vary from actual
            self.karma_comments = str(user_as_redditor.comment_karma) + " karma"
            self.karma_overall = str(user_as_redditor.link_karma + user_as_redditor.comment_karma) + " karma"
            #Is user a moderator
            self.moderator = False;
            if (user_as_redditor.is_mod):
                self.moderator = True;
            self.info_values = [self.name, self.cake_day, self.age, self.karma_comments, self.karma_overall, self.moderator, self.suspended, self.id]
            
    def IsSuspended(self):
        return self.suspended
    
    def ConvertBasicInfoToTxt(self):
        opened_file.write("\n" + self.txt_delimiter + "\n")
        for idx in range(0,len(self.info_keys)):
            opened_file.write(str(self.info_values[idx]) + ";,.")
        opened_file.write("\n" + self.txt_delimiter + "_close\n")
        
    def PrintBasicInfo(self):
        for idx in range(0,len(self.info_keys)):
            print(self.info_keys[idx] + str(self.info_values[idx]))
            
        
class TopFiveVotedSubmissionsData:
    descriptive_header: str
    info_keys: list
    info_values: list
    txt_delimiter: str
    
    def __init__(self, descriptive_header="\nTop 5 most upvoted posts (Out of last 99 posts):\n", txt_delimiter = "TopFiveVotedSubmissionsData_delim"):
        self.descriptive_header = descriptive_header
        self.info_keys = ["Rank ", "| Score: ", " | Time: ", " UTC | ", " comments | Title: "]
        self.info_values = []
        self.txt_delimiter = txt_delimiter
        
    def FindFiveMostVotedSubmissions(self):
        sorted_submissions = sorted(user_submissions_list,key=lambda x:x.score, reverse=True)
        idx = 0
        for submission in sorted_submissions:
            if idx < 5 and idx < len(sorted_submissions):
                self.info_values.append([idx + 1, submission.score, datetime.utcfromtimestamp(int(submission.created_utc)).strftime("%m/%d/%Y, %H:%M:%S"), submission.num_comments, submission.title])
            idx+=1
            
    def PrintFiveMostVotedSubmissions(self):
        print(self.descriptive_header)
        for idx in range(0,len(self.info_values)):
            to_print = ""
            for idx1 in range(0,len(self.info_keys)):
                to_print += self.info_keys[idx1] + str(self.info_values[idx][idx1])
            print(to_print)
            
    def ConvertFiveMostVotedSubmissionsToTxt(self):
        opened_file.write("\n" + self.txt_delimiter + "\n")
        for idx in range(0,len(self.info_values)):
            to_txt = "listbegin_delim"
            for idx1 in range(0,len(self.info_keys)):
                to_txt +=str(self.info_values[idx][idx1]) + ";,."
            to_txt += "list_delim_close\n"
            opened_file.write(to_txt)
        opened_file.write(self.txt_delimiter + "_close\n")
        
class TopFiveVotedCommentsData:
    descriptive_header: str
    info_keys: list
    info_values: list
    txt_delimiter: str
    def __init__(self, descriptive_header="\nTop 5 most upvoted comments (Out of last 99 posts):\n", txt_delimiter = "TopFiveVotedCommentsData_delim"):
        self.descriptive_header = descriptive_header
        self.info_keys = ["Rank ", "| Score: ", " | Time: ", " UTC | ", " replies | Contents: "]
        self.info_values = []
        self.txt_delimiter = txt_delimiter
        
    def FindFiveMostVotedComments(self):
        sorted_comments = sorted(user_comments_list,key=lambda x:x.score, reverse=True)
        idx = 0
        for comments in sorted_comments:
            if idx < 5 and idx < len(sorted_comments):
                self.info_values.append([idx + 1, comments.score, datetime.utcfromtimestamp(int(comments.created_utc)).strftime("%m/%d/%Y, %H:%M:%S"), len(comments.replies), comments.body.replace("\n","")[0:69]])
            idx+=1
        
    def PrintFiveMostVotedComments(self):
        print(self.descriptive_header)
        for idx in range(0,len(self.info_values)):
            to_print = ""
            for idx1 in range(0,len(self.info_keys)):
                to_print += self.info_keys[idx1] + str(self.info_values[idx][idx1])
            print(to_print)
            
    def ConvertFiveMostVotedCommentsToTxt(self):
        opened_file.write("\n" + self.txt_delimiter + "\n")
        for idx in range(0,len(self.info_values)):
            to_txt = "listbegin_delim"
            for idx1 in range(0,len(self.info_keys)):
                to_txt +=str(self.info_values[idx][idx1]) + ";,."
            to_txt += "list_delim_close\n"
            opened_file.write(to_txt)
        opened_file.write(self.txt_delimiter + "_close\n")
class VoteDistribution:
    descriptive_header: str
    txt_delimiter: str
    def __init__(self, descriptive_header="\nUser's top subreddits ranked by comment/submission upvotes (Out of last 198 interactions):\n", txt_delimiter = "VoteDistribution_delim"):
        self.descriptive_header = descriptive_header
        self.txt_delimiter = txt_delimiter
class MostActiveSubs:
    descriptive_header: str
    txt_delimiter: str
    def __init__(self, descriptive_header="\nTop active subreddits ranked by quantity of comments and submissions (Out of last 198 interactions):\n", txt_delimiter = "MostActiveSubs_delim"):
        self.descriptive_header = descriptive_header
        self.txt_delimiter = txt_delimiter

if __name__ == '__main__':
    print()
    user_name = GetUsernameInput()
    print()
    
    user_as_redditor = reddit.redditor(user_name)
    user_info = UserInfo()
    
    user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
    user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
    
    if user_info.IsSuspended():
        print("User is shadowbanned - only contains name and is_suspended attributes")
    else:
        user_info.SetBasicInfo()
        user_info.PrintBasicInfo()
        user_info.ConvertBasicInfoToTxt()
        
        u1 = TopFiveVotedSubmissionsData()
        u1.FindFiveMostVotedSubmissions()
        u1.PrintFiveMostVotedSubmissions()
        u1.ConvertFiveMostVotedSubmissionsToTxt()
        
        u2 = TopFiveVotedCommentsData()
        u2.FindFiveMostVotedComments()
        u2.PrintFiveMostVotedComments()
        u2.ConvertFiveMostVotedCommentsToTxt()
        
        user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
        user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
        print(FindVoteDistribution())
        
        user_comments_list = user_as_redditor.comments.new(limit=99) #Limited to 100 historical submissions by Reddit API
        user_submissions_list = user_as_redditor.submissions.new(limit=99) #Limited to 100 historical submissions by Reddit API
        print(FindMostActive())
    print("")
    opened_file.close()