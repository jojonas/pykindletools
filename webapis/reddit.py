import praw
import util
import datetime

class RedditBook(util.HTMLBook):
	def __init__(self, username):
		util.HTMLBook.__init__(self)
		self.reddit = praw.Reddit(user_agent="MOBI downloader by %s" % username)
		
	def gather(self):
		raise NotImplementedError("create() function not implemented.")
		
		
class RedditSelfSubredditBook(RedditBook):
	def __init__(self, username, subreddit, count=5):
		RedditBook.__init__(self, username)
		self.subreddit = subreddit
		self.count = count
		self.username = username
		
	def gather(self):
		self.addHeading("/r/%s" % self.subreddit)
		nowStr = datetime.datetime.now().strftime("%B %d, %Y, %H:%M")
		self.addHtml("<sup>(compiled by /u/%s on %s)</sup>" % (self.username, nowStr))
		submissions = self.reddit.get_subreddit(self.subreddit).get_hot(limit=self.count)
		for submission in submissions:
			self.addHtml("<hr />")
			self.addHeading(submission.title, 2)
			self.addHtml("<sup>(score: %d, submitted by /u/%s)</sup>" % (submission.score, submission.author.name))
			self.addHtml(submission.selftext_html)
