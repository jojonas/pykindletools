import praw
import util
import datetime
import collections

class RedditBook(util.HTMLBook):
	def __init__(self, username):
		util.HTMLBook.__init__(self)
		self.reddit = praw.Reddit(user_agent="MOBI downloader by %s" % username)
		
	def gather(self):
		raise NotImplementedError("create() function not implemented.")
		
		
class RedditSubredditBook(RedditBook):
	def __init__(self, username, subreddit, count=5):
		RedditBook.__init__(self, username)
		self.subreddit = subreddit
		self.count = count
		self.username = username
		self.posts = collections.OrderedDict()
		
	def gather(self):
		self.addHeading("/r/%s" % self.subreddit)
		nowStr = datetime.datetime.now().strftime("%B %d, %Y, %H:%M")
		self.addHtml("<sup>(compiled by /u/%s on %s)</sup>" % (self.username, nowStr))
		submissions = self.reddit.get_subreddit(self.subreddit).get_hot(limit=self.count)
		for i, submission in enumerate(submissions):
			self.addPagebreak()
			
			aname = "post%d" % i
			self.posts[aname] = submission.title
			self.addHtml("<a name='%s'></a>" % aname)
			
			self.addHeading(submission.title, 2)
			self.addHtml("<sup>(score: %d, submitted by /u/%s)</sup>" % (submission.score, submission.author.name))
			if submission.is_self:
				if submission.selftext_html is not None:
					html = self.htmlParser.unescape(submission.selftext_html)
					html = html.replace(" class=\"md\"", "")
					self.addHtml(html)
			else:
				self.addParagraph("<a href=\"%s\">%s</a>" % (submission.url, submission.url))
