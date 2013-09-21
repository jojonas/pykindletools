from util import make_filename

import os
import tempfile
from contextlib import contextmanager

class File:
	def __init__(self, title, ext='txt'):
		self.title = title
		self.extension = ext
		self.filename = "{title}.{ext}".format(title=make_filename(title), ext=ext)
		
	def content(self):
		raise NotImplementedError("content() missing.")
		return ''
		
	def write(self):
		with open(self.filename, 'wb') as file:
			file.write(self.content().encode('utf-8'))

	def delete(self):
		os.remove(self.filename)
		
	@contextmanager
	def tempObject(self):
		self.write()
		try:
			yield 
		finally:
			self.delete()
		