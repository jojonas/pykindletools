from pykindle.htmlgenerator import Book

import wikipedia

class WikipediaArticleBook(Book):
	def __init__(self, title):
		Book.__init__(self, u"Wikipedia: {title}".format(title=title))
		self.search_term = title
		self.page = None
		
	def gather(self):
		self.page = wikipedia.page(self.search_term)
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
			
	def setLanguage(self, lang):
		wikipedia.set_lang(lang)
		