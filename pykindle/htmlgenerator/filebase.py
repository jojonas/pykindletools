from pykindle.htmlgenerator.util import make_filename

import os
from contextlib import contextmanager
import codecs

class File(object):
	def __init__(self, title, ext='txt'):
		self.title = title
		self.extension = ext
		self.filename = "{title}.{ext}".format(
			title=make_filename(title), 
			ext=ext
		)
		
	def content(self):
		raise NotImplementedError("content() missing.")
		
	def write(self):
		with codecs.open(self.filename, "wb", "utf-8") as outfile:
			outfile.write(self.content())

	def delete(self):
		os.remove(self.filename)
		
	@contextmanager
	def tempObject(self):
		self.write()
		try:
			yield 
		finally:
			self.delete()
			
		