from pykindle.htmlgenerator import Book

import urllib2
import xmlrpclib
import re
from datetime import datetime

class WordpressBook(Book):
	def __init__(self, url, username, password):
		self.username = username
		self.password = password
		
		self.server = xmlrpclib.ServerProxy(url).wp
		meta = self.server.getUsersBlogs(self.username, self.password)[0]
		
		self.blog_title = meta['blogName']
		self.blog_id = meta['blogid']
		Book.__init__(self, "Wordpress: {title}".format(title=self.blog_title))
		
		
	def gather(self):
		self.addHeading(self.blog_title)
		
		posts = self.server.getPosts(self.blog_id, self.username, self.password)
		authorsCache = {}
		for post in posts:
			if not post['post_author'] in authorsCache:
				authorsCache[post['post_author'] ] = self.server.getUser(self.blog_id, self.username, self.password, post['post_author'] )
			username = authorsCache[post['post_author'] ]['username']
		
			content = post['post_content']
			content = content.replace('&nbsp;', ' ').replace('\n', '<br />')
			content = re.sub(r'\[[^\]]+\]', '', content)
			
			date = datetime.strptime(post['post_date'].value, '%Y%m%dT%H:%M:%S')
			
			self.addPagebreak()
			self.addHeading(post['post_title'], 2)
			self.addAuthoringInfo(author=username, date=date, verb="posted")
		
			self.html.addHtml(u'<div>{content}</div>'.format(content=content))
			
		