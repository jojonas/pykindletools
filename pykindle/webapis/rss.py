from pykindle.htmlgenerator import Book

import urllib2
import xml.etree.ElementTree

class RSSBook(Book):
	def __init__(self, url):
		data = urllib2.urlopen(url).read()
		self.etree = xml.etree.ElementTree.fromstring(data).find("./channel")
		
		self.rss_title = self.etree.find("./title").text.strip()
		Book.__init__(self, "RSS: {title}".format(title=self.rss_title)) # a little late...
		
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
			self.html.addHtml(u'<p>{desc}</p>'.format(desc=description.replace('&', '&amp;')))
			self.html.addHtml(u'<p><a href="{url}">link to article</a></p>'.format(url=self.html.escape(link)))
			
		#nowStr = datetime.now().strftime("%B %d, %Y, %H:%M")
		
				