import mobi
from constants import *
import io

class Book:
	def __init__(self):
		self.title = ""
		self.author = ""
		self.publisher = ""
		
		self.text_length = 0
		
		self.textBuffer = io.BytesIO()
		
	def _getNextTextRecord(self):
		opos = self.textBuffer.tell()
		self.textBuffer.seek(0, 2) # jump to end
		npos = min((opos+RECORD_SIZE), self.textBuffer.tell())
		self.textBuffer.seek(npos)
		extra = 0
		
		last = b''
		start = 0
		while not last.decode('utf-8', 'ignore'):
			self.textBuffer.seek(-start,2)
			last = self.textBuffer.read(start)
			start += 1
		
		try:
			last.decode('utf-8', 'strict')
		except UnicodeDecodeError:
			prev = start
			while True:
				text.textBuffer.seek(-prev,2)
				prev += 1
				last = self.textBuffer.read(prev)
				try:
					last.decode('utf-8')
				except UnicodeDecodeError:
					pass
				else:
					break
			extra = prev-start
			
		self.textBuffer.seek(opos)
		data = self.textBuffer.read(RECORD_SIZE)
		overlap = self.textBuffer.read(extra)
		self.textBuffer.seek(npos)
		
		return data, overlap
		
	def _createTextRecords(self):
		records = []
		
		self.textBuffer.seek(0)
		while self.textBuffer.tell() < self.text_length:
			data, overlap = self._getNextTextRecord()
			record = mobi.CompressedTrailingRecord(data, overlap)
			records.append(record)
		
		return records
		
	def _createRecord0(self):
		record0 = mobi.PalmDocRecord()
		record0.text_length = self.text_length
		
		record0.mobi.name = self.title
		
		record0.mobi.exth.records.append(mobi.ExthRecord(EXTH_RECORD_TYPE_AUTHOR, self.author))
		record0.mobi.exth.records.append(mobi.ExthRecord(EXTH_RECORD_TYPE_PUBLISHER, self.publisher))
		
		return record0
		
	def write(self, stream):
		book = mobi.PDBFile(self.title)
		
		# build book
		textRecords = self._createTextRecords()
		record0 = self._createRecord0()
		
		book.records.append(record0)
		for record in textRecords:
			book.records.append(record)			
		record0.mobi.last_content_record = len(book.records)-1
		record0.mobi.first_non_book_record = len(book.records)
		
		record0.mobi.flis_record = len(book.records)
		book.records.append(mobi.FLISRecord())
		
		record0.mobi.fcis_record = len(book.records)
		book.records.append(mobi.FCISRecord(self.text_length))
		
		book.records.append(mobi.EOFRecord())
		
		# fill rest information
		record0.text_record_count = len(textRecords)
		
		for counter, record in enumerate(book.records):
			record.id = counter
		
		# finish
		book.finish()
		stream.write(book.data())
		
	def addText(self, text):
		self.text_length += len(text)
		self.textBuffer.write(text)
		
		
if __name__=="__main__":
	book = Book()
	book.title = "Lorem Ipsum"
	book.author = "Max Mustermann"
	book.publisher = "My Verlag"
	
	with open("loremipsum.txt", "r") as input:
		for line in input:
			book.addText(line + "\r\n")
	
	with open("lorem.mobi", "wb") as file:
		book.write(file)