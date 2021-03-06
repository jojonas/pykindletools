from pykindle.htmlgenerator import Book

import praw

from urlparse import urlparse
from datetime import datetime

IMGUR_HOST = 'i.imgur.com'
REDDIT_LOGO = "http://www.redditstatic.com/about/assets/reddit-alien.svg"

class RedditSubredditBook(Book):
	"""Create a MOBI file from a subreddit.
	
	Arguments:
	:param subreddit: the subreddit that will be fetched
	:param username: your reddit username (for the crawler user agent, see documentation of reddit API)
	:param posts: number of posts that shall be fetched 
	:type int
	:param comments: number of comments that shall be fetched per post
	:type int
	"""
	def __init__(self, subreddit, username, posts=5, comments=5):
		Book.__init__(self, "Reddit: /r/{sr}".format(sr=subreddit))
		self.reddit = praw.Reddit(user_agent="MOBI downloader by %s" % username)
		
		self.subreddit = subreddit
		self.count = posts
		self.commentcount = comments
		self.username = username
		
		assert posts > 0
		assert comments >= 0
		
	def gather(self):
		self.addHeading(self.subreddit)
		
		self.addAuthoringInfo(
			author=self.username, 
			date=datetime.now(), 
			verb="compiled"
		)
		self.addImage(REDDIT_LOGO, width=0.5)
		
		submissions = \
			self.reddit.get_subreddit(self.subreddit).get_hot(limit=self.count)
			
		for submission in submissions:
			self.addPagebreak()
			self.addHeading(submission.title, 2)
			self.addAuthoringInfo(
				author="{author} ({score})".format(
					author=submission.author.name, 
					score=submission.score
				), 
				date=datetime.fromtimestamp(submission.created), 
				verb="submitted"
			)
			
			if submission.is_self:
				if submission.selftext_html is not None:
					html = self.html.unescape(submission.selftext_html)
					self.html.addHtml(html)
			else:
				url = urlparse(submission.url)
				if url.netloc == IMGUR_HOST and url.path.lower().endswith('jpg'):
					self.addImage(submission.url)
				else:
					self.html.addHtml(r'<p><a href="{url}">{url}</a></p>' \
						.format(url=self.html.escape(submission.url)))

			if self.commentcount > 0:
				self.addHeading("Comments", 3)
				for comment in submission.comments[:self.commentcount]:
					if not isinstance(comment, praw.objects.MoreComments):
						html = r'''<blockquote>
						{body}
						<footer>
							- {user} ({score})
						</footer>
						</blockquote>'''.format(
							user=self.html.escape(comment.author.name), 
							score=comment.score, 
							body=comment.body
						)
						self.html.addHtml(html)
					
					
				
				