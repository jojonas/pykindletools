from pykindle.htmlgenerator import Book

from datetime import datetime
import xml.dom.minidom
import re

from evernote.api.client import EvernoteClient, NoteStore
import evernote.edam.type.ttypes as Types

def clean_name(text):
	text = text.lower().strip()

class EvernoteBook(Book):
	"""Create a MOBI file from an Evernote note book.
	
	Arguments:
	:param token: OAuth/Developer token to Evernote 
	:param searchNotebook: (sub-)string to find the note book
	:param count: number of Notes to fetch
	:type int
	"""
	def __init__(self, token, searchNotebook, count=50):
		self.client = EvernoteClient(token=token)
		self.noteStore = self.client.get_note_store()
		
		found = []
		for notebook in self.noteStore.listNotebooks():
			if searchNotebook in notebook.name:
				found.append(notebook)
				
		if len(found) < 1:
			raise IOError("Notebook not found.")
		elif len(found) > 1:
			raise IOError("%d notebooks match the criteria." % len(found))
			
		self.notebook = found[0]
		
		Book.__init__(self, "Evernote: {title}".format( \
			title=self.notebook.name))
		
		self.count = count
		self.user = self.client.get_user_store().getUser()
		
	def gather(self):
		self.addHeading(self.notebook.name)
		
		filter = NoteStore.NoteFilter()
		filter.notebookGuid = self.notebook.guid
		
		resultSpec = NoteStore.NotesMetadataResultSpec()
		resultSpec.includeNotebookGuid	= True
		
		noteMetadatas = self.noteStore.findNotesMetadata(
			filter, 
			0, 
			self.count,
			resultSpec
		).notes
		
		for noteMetadata in noteMetadatas:
			note = self.noteStore.getNote(
				noteMetadata.guid, 
				True, 
				False, 
				False, 
				False
			)
			doc = xml.dom.minidom.parseString(note.content)
			
			self.addPagebreak()
			self.addHeading(note.title, 2)
			self.addAuthoringInfo(
				author=self.user.username, 
				date=datetime.fromtimestamp(note.updated/1000.0),
				verb="updated"
			)
			self.html.addHtml(doc.documentElement.toxml("utf-8").decode("utf-8"))
			