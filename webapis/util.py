import xml.dom.minidom
import HTMLParser

class HTMLBook:
	def __init__(self):
		self.document = xml.dom.minidom.Document()
		self._declLength = len(self.document.toxml())
		self.html = self.document.createElement('html')
		self.head = self.document.createElement('head')
		self.body = self.document.createElement('body')
		self.document.appendChild(self.html)
		self.html.appendChild(self.head)
		self.html.appendChild(self.body)
		self.htmlParser = HTMLParser.HTMLParser()
		
	def addHeading(self, text, level=1):
		self.addHtml("<h%d>%s</h%d>" % (level, text, level))
		
	def addParagraph(self, text):
		self.addHtml("<p>%s</p>" % text)
		
	def addHtml(self, html):
		data = xml.dom.minidom.parseString(self.htmlParser.unescape(html).encode('utf-8'))
		self.body.appendChild(data.documentElement)
		
	def toHtml(self):
		return self.document.toxml()[self._declLength:]

		