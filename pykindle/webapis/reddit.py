from pykindle.htmlgenerator import Book

import praw

from urlparse import urlparse
from datetime import datetime

IMGUR_HOST = 'i.imgur.com'
REDDIT_LOGO = "http://www.redditstatic.com/about/assets/reddit-alien.svg"

class RedditSubredditBook(Book):
	def __init__(self, username, subreddit, count=5):
		Book.__init__(self, "Reddit: /r/{sr}".format(sr=subreddit))
		self.reddit = praw.Reddit(user_agent="MOBI downloader by %s" % username)
		
		self.subreddit = subreddit
		self.count = count
		self.commentcount = 5
		self.username = username
		
	def gather(self):
		self.addHeading("/r/%s" % self.subreddit)
		nowStr = datetime.now().strftime("%B %d, %Y, %H:%M")
		self.html.addHtml("<small>(compiled by /u/{user} on {date})</small>".format(user=self.html.escape(self.username), date=self.html.escape(nowStr)))
		self.html.addHtml("<br/>")
		self.addImage(REDDIT_LOGO, width=0.8)
		
		submissions = self.reddit.get_subreddit(self.subreddit).get_hot(limit=self.count)
		for i, submission in enumerate(submissions):
			self.addPagebreak()
			self.addHeading(submission.title, 2)
			self.html.addHtml(r'<small>(score: {score}, submitted by /u/{user})</small>'.format(score=self.html.escape(submission.score), user=self.html.escape(submission.author.name)))
			
			if submission.is_self:
				if submission.selftext_html is not None:
					html = self.html.unescape(submission.selftext_html)
					self.html.addHtml(html)
			else:
				url = urlparse(submission.url)
				if url.netloc == IMGUR_HOST and url.path.lower().endswith('jpg'):
					self.addImage(submission.url)
				else:
					self.html.addHtml(r'<p><a href="{url}">{url}</a></p>'.format(url=self.html.escape(submission.url)))

			self.addHeading("Comments", 3)
			for comment in submission.comments[:self.commentcount]:
				if not isinstance(comment, praw.objects.MoreComments):
					self.html.addHtml(r'<blockquote>{body}<footer>- {user} ({score})</footer></blockquote>'.format(user=self.html.escape(comment.author.name), score=self.html.escape(comment.score), body=comment.body))
				
				
				
				