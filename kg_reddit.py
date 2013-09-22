from pykindle.webapis.reddit import RedditSubredditBook

import sys

def gather_posts(username, subreddit, count=5):
	book = RedditSubredditBook(username, subreddit, count)
	book.gather()
	book.createMobi()
	
if __name__=="__main__":
	if len(sys.argv) < 3:
		print "Usage: %s <username> <subreddit>" % sys.argv[0]
	else:
		gather_posts(sys.argv[1], sys.argv[2], 5)
		