from filebase import File

NCX_TEMPLATE = \
'''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="en">
	<docTitle>
		<text>{title}</text>
	</docTitle>
	<navMap>{navpoints}</navMap>
</ncx>'''

NCX_NAVPOINTS_TEMPLATE = \
'''<navPoint id="np_{counter}" playOrder="{counter}">
	<navLabel>
		<text>{title}</text>
	</navLabel>
	<content src="{htmlfile}#{aname}"/>
	{childvals}
</navPoint>'''

class TocEntry:
	def __init__(self, title, htmlfname, aname, level):
		self.title = title
		self.aname = aname
		self.htmlfname = htmlfname
		self.level = level
		
		self.parent = None
		self.children = []
		
	def toXml(self, counter):
		childVals = ''
		for child in self.children:
			xml, counter = child.toXml(counter)
			childVals += xml
		xml = NCX_NAVPOINTS_TEMPLATE.format(htmlfile=self.htmlfname, aname=self.aname, title=self.title, counter=counter, childvals=childVals)
		counter += 1
		return xml, counter

class NCXFile(File):
	def __init__(self, title):
		File.__init__(self, title, 'ncx')
		
		self.rootEntry = TocEntry('<dummy>', '<dummy>', '<dummy>', 0)
		self.lastTocEntry = self.rootEntry
	
	def content(self):
		return self.toXml()
		
	def addTocEntry(self, title, htmlfname, aname, level=1):
		if level <= 0:
			raise IndexError("TOC level must be greater than 0.")
		elif level > self.lastTocEntry.level + 1:
			raise IndexError("TOC entry of level %d cannot follow a TOC entry of level %d." % (newEntry.level, self.lastTocEntry.level))
			
		newEntry = TocEntry(title, htmlfname, aname, level)		
	
		addEntry = None
		if level > self.lastTocEntry.level:
			addEntry = self.lastTocEntry
		elif level == self.lastTocEntry.level:
			addEntry = self.lastTocEntry.parent
		else:
			addEntry = self.lastTocEntry
			while level <= addEntry.level:
				addEntry = addEntry.parent
			
		addEntry.children.append(newEntry)
		newEntry.parent = addEntry
		
		self.lastTocEntry = newEntry
		
	def toXml(self):
		navpoints_xml = ''
		counter = 1
		for entry in self.rootEntry.children:
			xml, counter = entry.toXml(counter)
			navpoints_xml += xml
			
		return NCX_TEMPLATE.format(title=self.title, navpoints=navpoints_xml)
		
	