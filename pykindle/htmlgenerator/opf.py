from filebase import File

OPF_TEMPLATE = \
'''<?xml version="1.0" encoding="utf-8"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="uid">
	<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
		{metatags}
		<meta name="output encoding" content="utf-8" />
	</metadata>
	<manifest>
		<item id="item0" href="{htmlname}" />
		<item id="ncx" href="{ncxname}"></item>
	</manifest>
	<spine toc="ncx">
		<itemref idref="item0"/>
	</spine>
	<tours>
	</tours>
	<guide>
		<reference title="Text" type="text"  href="{htmlname}" />
	</guide>
</package>'''

class OPFFile(File):
	def __init__(self, title):
		File.__init__(self, title, 'opf')
		self.html = None
		self.ncx = None
		self.metaInfos = {}
		
		self.addMetadata("title", title)
		self.addMetadata("language", "en")
		
	def content(self):
		return self.toXml()
	
	def addMetadata(self, key, value):
		self.metaInfos[key] = value
		
	def setHtml(self, html):
		self.html = html
		
	def setNcx(self, ncx):
		self.ncx = ncx
		
	def toXml(self):
		metatags = ''
		for key, value in self.metaInfos.iteritems():
			metatags += '<dc:{key}>{value}</dc:{key}>\n'.format(key=key, value=value)
		return OPF_TEMPLATE.format(htmlname=self.html.filename, ncxname=self.ncx.filename, title=self.title, metatags=metatags)