import xml.dom.minidom
import re
import HTMLParser

class HTMLBook:
	def __init__(self):
		self.document = xml.dom.minidom.Document()
		self._declLength = len(self.document.toxml())
		self.html = self.document.createElement('html')
		self.head = self.document.createElement('head')
		self.guide = self.document.createElement('guide')
		self.body = self.document.createElement('body')
		self.head.appendChild(self.guide)
		self.document.appendChild(self.html)
		self.html.appendChild(self.head)
		self.html.appendChild(self.body)
		self.htmlParser = HTMLParser.HTMLParser()
		
	def addHeading(self, text, level=1):
		self.addHtml("<h%d>%s</h%d>" % (level, text, level))
		
	def addParagraph(self, text, indent=None):
		style = ''
		if indent is not None:
			style = ' style="text-indent:%s"' % indent
		self.addHtml("<p%s>%s</p>" % (style, text))
		
	def addHtml(self, html):
		data = xml.dom.minidom.parseString(html.encode('utf-8'))
		imported = self.document.importNode(data.documentElement, True)
		self.body.appendChild(imported)
		
	def toHtml(self):
		html = self.document.toxml()[self._declLength:]
		html = re.sub(r">\s*<",r"><", html) 				# remove whitespace
		html = re.sub(r"<([^/>]+)/>", r"<\1></\1>", html) 	# remove self closing
		# http://stackoverflow.com/questions/97522/what-are-all-the-valid-self-closing-elements-in-xhtml-as-implemented-by-the-maj
		allowed_selfclose = ["area", "base", "br", "col", "embed", "hr", "img", "input", "keygen", "link", "menuitem", "meta", "param", "source", "track", "wbr"]
		allowed_selfclose += ["basefont", "bgsound", "frame", "isindex"]
		allowed_selfclose += ["mbp:pagebreak"]
		for tag in allowed_selfclose:
			html = html.replace("<%s></%s>" % (tag,tag), "<%s/>" % tag)
		return html

	def addPagebreak(self):
		pb = self.document.createElementNS('', 'mbp:pagebreak')
		self.body.appendChild(pb)
		