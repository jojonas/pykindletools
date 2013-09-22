from pykindle.htmlgenerator import Book

import wikipedia

class WikipediaArticleBook(Book):
	def __init__(self, title):
		Book.__init__(self, u"Wikipedia: {title}".format(title=title))
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
			