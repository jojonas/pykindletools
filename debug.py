import mobitools.lz77
from mobitools.util import debug_data
import re, struct

def find(stream, needle, after=False):
	offset = stream.tell()
	lneedle = len(needle)
	while True:
		chunk = stream.read(lneedle)
		if len(chunk) == 0:
			raise RuntimeError("'%s' not found in stream." % needle)
		if chunk == needle:
			break
		else:
			offset += 1
			stream.seek(offset)
	
	
	if after:
		offset += len(needle)
		
	stream.seek(offset)	
	return offset

def unpack_stream(stream, fmt):
	length = struct.calcsize(fmt)
	return struct.unpack(fmt, stream.read(length))
	
	
	
def dump_data(c):
	str = ""
	try:
		str += u"String: '%s'; " % c
	except UnicodeDecodeError:
		str += "String: non-utf8; "
	str += "Hex: %s; " % " ".join("%02x" % ord(x) for x in c) 
	str += "Dec: %s; " % " ".join("%d" % ord(x) for x in c) 
	str += "uInt: %d; " % struct.unpack('>I', c)[0]
	str += "Int: %d; " % struct.unpack('>i', c)[0]
	str += "Shorts: %d, %d; " % struct.unpack('>HH', c)
	return str
	
def print_exth(stream):
	stream.seek(0)
	
	exthOffset = find(stream, 'EXTH', after=True)
	
	headerSize, count = unpack_stream(stream, '>II')
	print "%d EXTH records, with a total length of %d bytes." % (count, headerSize)
	print "-"*50
	for i in xrange(count):
		type, size = unpack_stream(stream, '>II')
		size -= 8
		print "-"*50
		print " Type:", type
		print "-"*50
		
		if size > 0:
			data, = unpack_stream(stream, '%ds' % size)
			dataStr = debug_data(data)
		else:
			dataStr = 'NO DATA'
			
		print dataStr
		print "-"*50
		
	stream.seek(exthOffset + headerSize)
	
def dissect_html(stream, out):
	START_TOKEN = '<html>'
	END_TOKEN = '</html>'
	start = find(stream, START_TOKEN)
	data = mobitools.lz77.lz77_decompress(stream)
	end = data.find(END_TOKEN)
	data = data[:end+len(END_TOKEN)]
	
	data = re.sub(">\s*<","><", data)
	data = data.replace("<", "\n<")
	
	out.write(data)
		
def list_records(stream, preview_size=4):
	stream.seek(0)
	
	find(stream, "BOOKMOBI", after=True)
	stream.read(8) # unique id, nextRecordID
	nrecords = unpack_stream(stream, '>H')[0]
	records = []
	for i in xrange(nrecords):
		offset, id = unpack_stream(stream, '>II')
		id = id & 0x00FFFFFF
		records.append((id, offset))
	
	for id, offset in records:
		stream.seek(offset)
		data = stream.read(preview_size)
		print "-"*50
		print " ID:", id
		print " Offset:", offset
		print "-"*50
		print debug_data(data)
		print "-"*50
		
if __name__=="__main__":
	with open("talesfromtechsupport-kg.mobi", "rb") as file:
		print_exth(file)
		list_records(file)
	#parse("talesfromtechsupport-kg.mobi", "kg.html")
	#parse("talesfromtechsupport-nkg.mobi", "nkg.html")
	