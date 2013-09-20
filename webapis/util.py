import xml.dom.minidom
import HTMLParser

class HTMLBook:
	def __init__(self):
		self.document = xml.dom.minidom.Document()
		self._declLength = len(self.document.toxml())
		self.html = self.document.createElement('html')
		self.head = self.document.createElement('head')
		self.guide = self.document.createElement('guide')
		self.body = self.document.createElement('body')
		self.document.appendChild(self.html)
		self.html.appendChild(self.head)
		self.head.appendChild(self.guide)
		self.html.appendChild(self.body)
		self.htmlParser = HTMLParser.HTMLParser()
		
	def addHeading(self, text, level=1):
		self.addHtml("<h%d>%s</h%d>" % (level, text, level))
		
	def addParagraph(self, text, indent=False):
		style = ''
		if indent:
			style = ' style="bordler-left: 1px solid black"'
		self.addHtml("<p%s>%s</p>" % (style, text))
		
	def addHtml(self, html):
		data = xml.dom.minidom.parseString(html.encode('utf-8'))
		self.body.appendChild(data.documentElement)
		
	def toHtml(self):
		html = self.document.toxml()[self._declLength:]
		return html

	def addPagebreak(self):
		pb = self.document.createElementNS('', 'mbp:pagebreak')
		self.body.appendChild(pb)
		