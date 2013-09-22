from html import HTMLFile
from ncx import NCXFile
from opf import OPFFile

from contextlib import contextmanager
from util import call_kindlegen

import collections
import os, os.path
import urllib

class Book:
	def __init__(self, title):
		self.title = title
		self.html = HTMLFile(title)
		self.opf = OPFFile(title)
		self.ncx = NCXFile(title)
		
		self.opf.setHtml(self.html)
		self.opf.setNcx(self.ncx)
		
		self.counters = collections.defaultdict(int)
		
		self.images = {}
		
	def generateId(self, category='object'):
		self.counters[category] += 1
		return "{category}{counter}".format(category=category, counter=self.counters[category])
		
	def addHeading(self, text, level=1):
		if not (1 <= level <= 6):
			raise IndexError("level %d is illegal." % level)
			
		self.addTocEntry(text, level)
		self.html.addHtml(u'<h{lvl}>{heading}</h{lvl}>'.format(lvl=level, heading=self.html.escape(text)))
		
	def addParagraph(self, text, indent=None):
		style = ''
		
		if indent is not None:
			indent = re.sub(r'[<>"/]', r'', indent)
			style = ' style="text-indent: {indent}"'.format(indent=indent)
			
		self.html.addHtml(u'<p{style}>{content}</p>'.format(style=style, content=self.html.escape(text)))
		
	def addImage(self, src, width=0.95, center=True):
		_, ext = os.path.splitext(src)
		id = self.generateId("image") + ext
		self.images[id] = src
		
		html = u'<img src="{id}" width="{widthpercent}%%" />'.format(id=id, widthpercent=int(width*100.0))
		if center:
			html = u'<p style="text-align: center">{html}</p>'.format(html=html)
		self.html.addHtml(html)
		
	def addTocEntry(self, title, level=1):
		id = self.generateId("anchor")
		self.ncx.addTocEntry(title, self.html.filename, id, level)
		self.html.addHtml(u'<a name="{id}"></a>'.format(id=id))
		
	def addPagebreak(self):
		# this shouldn't be in this class
		pb = self.html.document.createElementNS('', 'mbp:pagebreak')
		self.html.body.appendChild(pb)
		
	@contextmanager
	def tempObject(self):
		for tempName, src in self.images.iteritems():
			urllib.urlretrieve(src, tempName)
		yield
		for tempName in self.images.keys():
			os.remove(tempName)
		
	def createMobi(self):
		with self.tempObject():
			with self.html.tempObject():
				with self.ncx.tempObject():
					with self.opf.tempObject():
						call_kindlegen(self.opf.filename)
					
			