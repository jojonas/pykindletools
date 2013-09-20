from mobitools import Book
from webapis.reddit import RedditSelfSubredditBook

import sys

def gather_selfposts(username, subreddit, count=5):
	rssb = RedditSelfSubredditBook(username, subreddit, count)
	rssb.gather()
	
	book = Book()
	book.title = "/r/%s" % subreddit
	book.author = "/u/%s" % username
	
	html = rssb.toHtml()
	book.addText(html)
	
	with open("%s.mobi" % subreddit, "wb") as file:
		book.write(file)
	
if __name__=="__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <username>" % sys.argv[0]
	else:
		gather_selfposts(sys.argv[1], "talesfromtechsupport", 5)