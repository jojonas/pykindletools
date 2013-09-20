from mobitools import Book
from webapis.reddit import RedditSubredditBook

import sys

def gather_posts(username, subreddit, count=5):
	rssb = RedditSubredditBook(username, subreddit, count)
	rssb.gather()
	
	book = Book()
	book.title = "/r/%s" % subreddit
	book.author = "/u/%s" % username
	
	html = rssb.toHtml()
	book.addText(html)
	
	with open("%s.mobi" % subreddit, "wb") as file:
		book.write(file)
	
if __name__=="__main__":
	if len(sys.argv) < 3:
		print "Usage: %s <username> <subreddit>" % sys.argv[0]
	else:
		gather_posts(sys.argv[1], sys.argv[2], 50)