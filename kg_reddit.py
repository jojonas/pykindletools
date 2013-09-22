from pykindle.webapis.reddit import RedditSubredditBook

import argparse

parser = argparse.ArgumentParser(description="Create a MOBI file from a subreddit.")
parser.add_argument('subreddit', help="the subreddit that will be fetched")
parser.add_argument('username', help="your reddit username (for the crawler user agent, see documentation of reddit API)")
parser.add_argument('-n, --posts', metavar='COUNT', help="number of posts that shall be fetched", default=5, type=int, dest='posts')
parser.add_argument('-c, --comments', metavar='COUNT', help="number of comments that shall be fetched per post", default=5, type=int, dest='comments')
parser.add_argument('-k, --kindlegen', metavar='EXE', help="location of kindlegen.exe", default="kindlegen.exe", dest='kindlegen')

args = parser.parse_args()

book = RedditSubredditBook(args.username, args.subreddit, args.posts, args.comments)
book.setKindlegen(args.kindlegen)
book.gather()
book.createMobi()
	