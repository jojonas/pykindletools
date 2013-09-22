from pykindle.htmlgenerator import Book

import wikipedia

class WikipediaArticleBook(Book):
	"""Create a MOBI file from a Wikipedia article.
	
	Arguments:
	:param title: Search term for Wikipedia
	:param lang: Wikipedia language
	"""
	def __init__(self, title, lang="en"):
		Book.__init__(self, u"Wikipedia: {title}".format(title=title))
		wikipedia.set_lang(lang)
		self.page = wikipedia.page(title)
		
	def gather(self):
		self.addHeading(self.page.title)
		
		content = self.page.content
		for line in content.split("\n"):
			level = 0
			if line.startswith('='):
				while line[0] == '=':
					level += 1
					line = line[1:-1]
				title = line[1:-1]
				self.addHeading(title, level)
			else:
				self.addParagraph(line)
				
		