import container
import constants
import lz77
import util

import time, struct, random

class PDBFile(container.SerializedContainer):
	def __init__(self, name):
		container.SerializedContainer.__init__(self)
		
		# have to be set
		self.name = name
		
		# others
		self.records = []
		
	def serialize(self):
		for counter, record in enumerate(self.records):
			record.finish()
			
		now = int(time.time())

		data = ''
		data += struct.pack(b'32s', self.name[:31])
		data += struct.pack(b'>HHIIIIII', 0, 0, now, now, 0, 0, 0, 0)
		data += b'BOOKMOBI'
		data += struct.pack(b'>IIH', 2*len(self.records)-1, 0, len(self.records))
		
		offset0 = len(data) + 8*len(self.records) + 2
		offset = offset0
		for record in self.records:
			data += struct.pack(b'>I', offset)
			data += struct.pack(b'>I', record.id + ((record.attributes & 0xff) << (3*8)))
			offset += record.length()
		data += b'\0\0'
		
		assert len(data) == offset0
		for record in self.records:
			data += record.data()
			
		return data

		
class PDBRecord(container.SerializedContainer):
	def __init__(self):
		container.SerializedContainer.__init__(self)
		self.id = 0
		self.attributes = 0
	
		
class CompressedTrailingRecord(PDBRecord):
	def __init__(self, uncompressed, overlap):
		PDBRecord.__init__(self)
		self.uncompressed = uncompressed
		self.overlap = overlap
	
	def serialize(self):
		data = lz77.lz77_compress(self.uncompressed)
		assert len(self.overlap) <= 3
		data += self.overlap
		data += util.variable_width_int_backwards(len(self.overlap))
		return data
		
class PalmDocRecord(PDBRecord):
	def __init__(self):
		PDBRecord.__init__(self)
		
		self.mobi = MobiHeader()
		self.text_length = 0 # ::TODO::
		self.text_record_count = 0 # ::TODO::
		
		# do not change
		self.reading_position = 0
	
	def serialize(self):
		self.mobi.finish()
		
		data = ''
		data += struct.pack(b'>H', 2)
		data += b'\0\0'
		data += struct.pack(b'>I', self.text_length)
		data += struct.pack(b'>H', self.text_record_count)
		data += struct.pack(b'>H', constants.RECORD_SIZE)
		data += struct.pack(b'>I', self.reading_position)
		
		data += self.mobi.data()
		
		return data
		
class MobiHeader(container.SerializedContainer):
	def __init__(self):
		container.SerializedContainer.__init__(self)
		
		self.name = ""
		
		self.type = constants.MOBI_TYPE_BOOK
		self.id = random.randint(0, 0xFFFFFFFF)
		self.version = 8
		self.exth = ExthHeader()
		self.min_version = self.version
		self.first_content_record = 1
		self.extra_flags = constants.TRAILING_MULTIBYTE
		self.first_image_record = 0
		
		self.last_content_record = 0 
		self.fcis_record = 0 
		self.flis_record = 0 
		self.indx_record = 0xFFFFFFFF
		
		# do not touch
		self.first_non_book_record = 0
		self.locale = constants.LOCALE_ENGLISH
		
	def serialize(self):
		self.exth.finish()
		
		nameData = self.name + b'\0\0'
		while len(nameData) % 4 > 0:
			nameData += '\0'
		
		data = b'MOBI'
		predictedLength = 232
		data += struct.pack(b'>I', predictedLength)
		
		data += struct.pack(b'>I', self.type)
		data += struct.pack(b'>I', constants.ENCODING_UTF8)
		data += struct.pack(b'>I', self.id)
		data += struct.pack(b'>I', self.version)
		
		data += b'\xff'*4*10
		
		data += struct.pack(b'>I', self.first_non_book_record)	# ::TODO::
		
		titleOffset = 16 + predictedLength + self.exth.length()
		data += struct.pack(b'>I', titleOffset)
		data += struct.pack(b'>I', len(self.name))
		data += struct.pack(b'>III', self.locale, 0,0)
		data += struct.pack(b'>I', self.min_version)
		data += struct.pack(b'>I', self.first_image_record)
		data += b'\0'*4*4 # huffman info (not supported yet)
		
		data += struct.pack(b'>I', 1 << 6) # exth info (??) ::TODO::
		data += b'\0'*32 #unknown
	
		data += b'\xff'*4*2 + b'\0'*4*5
		
		data += struct.pack(b'>HHI', self.first_content_record, self.last_content_record, 1)
		data += struct.pack(b'>II', self.fcis_record, 1)
		data += struct.pack(b'>II', self.flis_record, 1)
		
		data += b'\0'*4*2 + b'\xff'*4 + b'\0'*4 + b'\xff'*4*2
		
		data += struct.pack(b'>I', self.extra_flags)
		data += struct.pack(b'>I', self.indx_record)
		
		assert len(data) == predictedLength
		
		data += self.exth.data()
		
		assert len(data)+16 == titleOffset
		data += nameData
		
		while len(data) % 4 > 0:
			data += b'\0'
		
		return data
		
class ExthHeader(container.SerializedContainer):
	def __init__(self):
		container.SerializedContainer.__init__(self)
		self.records = []
		
	def serialize(self):
		length = 0
		for record in self.records:
			record.finish()
			length += record.length()
			
		data = b'EXTH'
		predictedLength = length + 12
		data += struct.pack(b'>I', predictedLength)
		data += struct.pack(b'>I', len(self.records))
		for record in self.records:
			data += record.data()
			
		assert len(data) == predictedLength
			
		while len(data) % 4 > 0:
			data += '\0'
		return data
		
class ExthRecord(container.SerializedContainer):
	def __init__(self, type, data):
		container.SerializedContainer.__init__(self)
		self.type = type
		if isinstance(data, int):
			data = struct.pack(b'>I', data)
		self.raw = data
		
	def serialize(self):
		data = ''
		data += struct.pack(b'>I', self.type)
		data += struct.pack(b'>I', len(self.raw)+8)
		data += self.raw
		return data
		
class EOFRecord(PDBRecord):
	def serialize(self):
		return b'\xe9\x8e\r\n'
		
class FCISRecord(PDBRecord):
	def __init__(self, l):
		PDBRecord.__init__(self)
		self.text_length = l
			
	def serialize(self):
		data = b'FCIS\x00\x00\x00\x14\x00\x00\x00\x10\x00\x00\x00\x02\x00\x00\x00\x00'
		data += struct.pack(b'>I', self.text_length)
		data += b'\x00\x00\x00\x00\x00\x00\x00\x28\x00\x00\x00\x00\x00\x00\x00'
		data += b'\x28\x00\x00\x00\x08\x00\x01\x00\x01\x00\x00\x00\x00'
		return data
		
class FLISRecord(PDBRecord):
	def serialize(self):
		return b'FLIS\0\0\0\x08\0\x41\0\0\0\0\0\0\xff\xff\xff\xff\0\x01\0\x03\0\0\0\x03\0\0\0\x01'+ b'\xff'*4
		