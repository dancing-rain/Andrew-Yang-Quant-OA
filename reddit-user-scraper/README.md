# Reddit Subreddit Scraper

**Difficulty: 3**

Thank you for applying to Quant! We are very interested in your application and wanted to see what you can do with the skills and knowledge you possess. Please read through the following prompt for what to do.

## **Prompt: Reddit User Scraper**
The rise of retail trading and tracking this information dessimination has often been at the center of attention for those looking to track what others are doing. Reddit has been in the news lately in regards to how groups of retail traders are able to share their sentiment about the stock through its communications platform. Especially of note are certain highly influential users who have a significant following or reaction when they post. We want to be able to use this information to make insights into our positions.

Your task is to build a Python scraper for Reddit using its API. The goal of this script will be to gather information about pertinent users that we can use later as part of our Quantitative Research division. Your scrape should gather data about a user, namely any Public Identifying Information (user name, age, cake day, etc.), the most-voted posts, the most-voted replies, how the user votes depending on subreddit, and any other information that is possible. We need to be able to parse these, maybe as dataclass objects, and then it needs to be output into a fast, parsable file format (could be JSON or CSV for example). 

You will be graded on how fast your code runs, the ability to "future-proof" it, and the easeness that one unfamiliar with your code base can run your program in addition to the criteria listed below. This means it would also be wise to include some information on how to run your code, what your code does, and maybe even a section stating what future improvements would be in case someone else hops on your project.

To start working on your project, **make sure you have forked the repository so that you will own your own version**. If you have any questions, feel free to contact us.

## **Resources**
- https://www.reddit.com/dev/api/
- https://praw.readthedocs.io/en/stable/
- https://www.youtube.com/watch?v=vBH6GRJ1REM
test

## **Deliverables**
Your python application/script should do the following:
- Be able to accept command line arguments to pass in a user (e.g. "u/roaringkitty")
- Parse the user to obtain the following information in as few calls as possible:
  - PII: username, age, cake day, karma, etc.
  - top 5 most-voted (positive or negative) posts
  - top 5 most-voted replies
  - User's upvote/downvote distribution with respect to subreddits
  - which subreddits the user is most active on
  - any additional metrics you think might be useful!
- Store all data into easily parsable and logically organized objects
- Output data into a file with logical parsing
- As part of your python application, add a script that will help parse the file with respect to your data class

Optional requirements:
- Create a script that will expose this as an API
- Add your own pyenv with all environment requirements
- Be able to pass in a txt file with names of users instead of one-by-one
- Be able to use regex to dynamically search for users, ideally in addition to the above bullet.
- Recommend similar users if a user is mispelled

## **Grading**
We will be looking at your project and grading it under these five criteria:
1. Code
   - If it works
   - Modular
   - Follows best practices (ie. OOP)
2. Documentation
   - Concise and exact
   - Follows popular conventions
3. Styling
   - Human readable
   - Can quickly glance to receive all relevant information
   - Follows Google Style Guide (preferred if it exists) or most popular convention (ie. PEP8)
4. Robustness
   - Customizable
   - No technical debt (future proof)
   - Handles bad inputs and errors
5. Git
   - [Good commit messages](https://cbea.ms/git-commit/#seven-rules)
   - Commits are properly sized

For a full list of the grading criteria, please see the following [document](https://docs.google.com/spreadsheets/d/16CqSJSlch7w9q4_ZTiydKGk0T01rgvIEcHHwqsI_KSo/edit?usp=sharing). 