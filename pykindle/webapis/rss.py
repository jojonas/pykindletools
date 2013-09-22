from pykindle.htmlgenerator import Book

import urllib2
import xml.etree.ElementTree
from datetime import datetime

class RSSBook(Book):
	"""Create a MOBI file from a RSS 2.0 feed.
	
	Arguments:
	:param url: the url of the RSS feed
	"""
	def __init__(self, url):
		data = urllib2.urlopen(url).read()
		self.etree = xml.etree.ElementTree.fromstring(data).find("./channel")
		
		self.rss_title = self.etree.find("./title").text.strip()
		# a little late...
		Book.__init__(self, "RSS: {title}".format(title=self.rss_title)) 
		
	def gather(self):
		try:
			language = self.etree.find("./language").text
			self.opf.setMetadata("language", language)
		except AttributeError:
			pass
			
		try:
			language = self.etree.find("./description").text
			self.opf.setMetadata("Description", language)
		except AttributeError:
			pass
			
		self.addHeading(self.rss_title)
		
		try:
			dateStr = self.etree.find("./pubDate").text
			date = datetime.strptime(dateStr[:-6], '%a, %d %b %Y %H:%M:%S')
			self.addAuthoringInfo(date=date, verb="published")
		except AttributeError:
			pass
		
		try:
			image = self.etree.find("./image/url").text
			self.addImage(image)
		except AttributeError:
			pass
			
		for item in self.etree.findall("./item"):
			title = item.find("./title").text
			description = item.find("./description").text
			link = item.find("./link").text
			
			self.addPagebreak()
			self.addHeading(title, 2)
			self.html.addHtml(u'<div>{desc}</div>'.format(
				desc=description.replace('&', '&amp;'))
			)
			html = u'''<p>
				<a href="{url}">link to article</a>
				</p>'''.format(url=self.html.escape(link))
			self.html.addHtml(html)
			
				