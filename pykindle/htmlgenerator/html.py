from filebase import File

import xml.dom.minidom
import re
import HTMLParser, cgi

def walkTree(root, function):
	function(root)
	if root.childNodes:
		for node in root.childNodes:
			if node.nodeType == node.ELEMENT_NODE:
				walkTree(node, function)
				
class HTMLFile(File):
	def __init__(self, title):
		File.__init__(self, title, 'html')
		
		self.document = xml.dom.minidom.Document()
		self._declLength = len(self.document.toxml())
		self.html = self.document.createElement('html')
		self.head = self.document.createElement('head')
		self.body = self.document.createElement('body')
		self.document.appendChild(self.html)
		self.html.appendChild(self.head)
		self.html.appendChild(self.body)
		
		titleTag = self.document.createElement('title')
		titleTagText = self.document.createTextNode(title)
		titleTag.appendChild(titleTagText)
		self.head.appendChild(titleTag)
		
		metaEncoding = self.document.createElement('meta')
		metaEncoding.setAttribute('http-equiv', 'content-type')
		metaEncoding.setAttribute('content', 'text/html; charset=utf-8')
		self.head.appendChild(metaEncoding)
		
		self.htmlParser = HTMLParser.HTMLParser()
		
	def content(self):
		return self.exportHtml()

	def escape(self, txt):
		return cgi.escape(txt)
		
	def unescape(self, txt):
		return self.htmlParser.unescape(txt)
	
	def addHtml(self, html):
		data = xml.dom.minidom.parseString(html.encode("utf-8"))
		imported = self.document.importNode(data.documentElement, True)
		self.body.appendChild(imported)
		
	def removeAttributes(self, attribs=("id", "class")):
		def rmAttribs(node):
			for attrib in attribs:
				if node.hasAttribute(attrib):
					node.removeAttribute(attrib)		
		walkTree(self.document.documentElement, rmAttribs)
		
	def toHtml(self):
		return self.document.toxml("utf-8")[self._declLength:].decode("utf-8")
		
	def exportHtml(self):
		self.removeAttributes()
		html = self.toHtml()
		
		html = re.sub(r'>\s*<',r'><', html) 				# remove whitespace
		html = re.sub(r'[\t\n\r\f\v]',r' ', html) 			# remove all whitespace that is not a space
		html = re.sub(r'<([^/>]+)/>', r'<\1></\1>', html) 	# remove self closing
		
		# http://stackoverflow.com/questions/97522/what-are-all-the-valid-self-closing-elements-in-xhtml-as-implemented-by-the-maj
		allowed_selfclose = ["area", "base", "br", "col", "embed", "hr", "img", "input", "keygen", "link", "menuitem", "meta", "param", "source", "track", "wbr"]
		allowed_selfclose += ["basefont", "bgsound", "frame", "isindex"]
		allowed_selfclose += ["mbp:pagebreak"]
		for tag in allowed_selfclose:
			html = html.replace(u"<{tag}></{tag}>".format(tag=tag), u"<{tag}/>".format(tag=tag))
			
		return html

		
		