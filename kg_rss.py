import pykindle.webapis

import sys

def gather_rss(url):
	book = pykindle.webapis.rss.RSSBook(url)
	book.gather()
	book.createMobi()
	
if __name__=="__main__":
	if len(sys.argv) < 2:
		print "Usage: %s <url>" % sys.argv[0]
	else:
		gather_rss(sys.argv[1])
		