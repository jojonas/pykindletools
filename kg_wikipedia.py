import pykindle.webapis

import sys

def gather_article(title):
	book = pykindle.webapis.wikipedia.WikipediaArticleBook(title)
	book.gather()
	book.createMobi()
	
if __name__=="__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <article>" % sys.argv[0]
	else:
		gather_article(sys.argv[1])
		