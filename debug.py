import mobitools.lz77
import re, struct, collections, io
import contextlib

def unpack_multi(fmt, data):
	size = struct.calcsize(fmt)
		
	if len(data) % size == 0:
		tuple = struct.unpack(fmt * (len(data)/size), data)
		return tuple
	else:
		raise RuntimeError("Does not fit.")
	
		
def debug_data(data):
	infos = collections.OrderedDict()
	
	infos['length'] 			=  lambda d: len(d)
	infos['string'] 			=  lambda d: "'%s'" % str(d)
	infos['repr'] 				=  lambda d: "'%s'" % repr(d)
	infos['hex'] 				=  lambda d: tuple("%02x" % ord(c) for c in d)
	infos['dec'] 				=  lambda d: tuple(ord(c) for c in d)
	infos['char'] 				=  lambda d: unpack_multi('c', d)
	infos['signed char'] 		=  lambda d: unpack_multi('b', d)
	infos['unsigned char']	 	=  lambda d: unpack_multi('B', d)
	infos['bool'] 				=  lambda d: unpack_multi('?', d)
	infos['short'] 				=  lambda d: unpack_multi('h', d)
	infos['unsigned short']		=  lambda d: unpack_multi('H', d)
	infos['int'] 				=  lambda d: unpack_multi('i', d)
	infos['unsigned int'] 		=  lambda d: unpack_multi('I', d)
	infos['long'] 				=  lambda d: unpack_multi('l', d)
	infos['unsigned long'] 		=  lambda d: unpack_multi('L', d)
	infos['long long'] 			=  lambda d: unpack_multi('q', d)
	infos['unsigned long long'] =  lambda d: unpack_multi('Q', d)
	infos['float'] 				=  lambda d: unpack_multi('f', d)
	infos['double'] 			=  lambda d: unpack_multi('d', d)

	retval = ''
	for key, value in infos.iteritems():
		try:
			retval += " {:20}:   {}\n".format(key, str(value(data)))
		except RuntimeError:
			pass
	return retval

	
def find(stream, needle, after=False):
	offset = stream.tell()
	lneedle = len(needle)
	while True:
		chunk = stream.read(lneedle)
		if len(chunk) == 0:
			raise EOFError("'%s' not found in stream." % needle)
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
	
def get_records(stream):
	opos = stream.tell()
	
	stream.seek(0)
	find(stream, "BOOKMOBI", after=True)
	stream.read(8) # unique id, nextRecordID
	nrecords = unpack_stream(stream, '>H')[0]
	records = collections.OrderedDict()
	for i in xrange(nrecords):
		offset, attribid = unpack_stream(stream, '>II')
		id = attribid & 0x00FFFFFF
		attributes = (attribid & 0xFF000000) >> 6
		records[id] = (attributes, offset)

	stream.seek(opos)
	return records
	
def dump_data(c):
	output = ""
	try:
		output += u"String: '%s'; " % c
	except UnicodeDecodeError:
		output += "String: non-utf8; "
	output += "Hex: %s; " % " ".join("%02x" % ord(x) for x in c) 
	output += "Dec: %s; " % " ".join("%d" % ord(x) for x in c) 
	output += "uInt: %d; " % struct.unpack('>I', c)[0]
	output += "Int: %d; " % struct.unpack('>i', c)[0]
	output += "Shorts: %d, %d; " % struct.unpack('>HH', c)
	return output
	
def dump_exth(stream):
	output = ""
	stream.seek(0)
	exthOffset = find(stream, 'EXTH', after=True)
	headerSize, count = unpack_stream(stream, '>II')
	output += "="*50 + "\n"
	output += "  EXTH Header\n"
	output += "="*50 + "\n"
	output += "%d EXTH records, with a total length of %d bytes.\n" % (count, headerSize)
	output += "-"*50 + "\n"
	for i in xrange(count):
		type, size = unpack_stream(stream, '>II')
		size -= 8
		output += "-"*50 + "\n"
		output += " Type: %d\n" % type
		output += "-"*50 + "\n"
		
		if size > 0:
			data, = unpack_stream(stream, '%ds' % size)
			dataStr = debug_data(data)
		else:
			dataStr = 'NO DATA'
			
		output += dataStr + "\n"
		output += "-"*50 + "\n"
	stream.seek(exthOffset + headerSize)
	return output
	
	
def dump_html(stream, skip=0):
	START_TOKEN = b'<html>'
	END_TOKEN = b'</html>'
	
	stream.seek(0)
	find(stream, START_TOKEN, after=True)
	try:
		for i in xrange(skip):
			find(stream, START_TOKEN, after=True)
	except EOFError:
		return ''
	stream.seek(-len(START_TOKEN), 1)
	#print "SKIP",skip, "LOC", stream.tell()
		
	data = mobitools.lz77.lz77_decompress(stream)
	
	loc = data.find(END_TOKEN)
	if loc != -1:
		loc += len(END_TOKEN)
		data = data[:loc]
	
	data = re.sub(">\s*<","><", data)
	data = data.replace("<", "\n<")
	
	return data
	
		
def dump_record_info(stream, preview_size=4):
	output = ""
	output += "="*50 + "\n"
	output += "  PDB Records\n"
	output += "="*50 + "\n"
	records = get_records(stream)
	
	for id, (attributes, offset) in records.iteritems():
		stream.seek(offset)
		data = stream.read(preview_size)
		output += "-"*50 + "\n"
		output += " ID: %d\n" % id
		output += " Offset: %d\n" % offset
		output += " Attributes: %d\n" % attributes
		output += "-"*50 + "\n"
		output += debug_data(data)
		output += "-"*50 + "\n"
	
	return output
		
if __name__=="__main__":
	import sys
	fname = sys.argv[1]
	with open(fname, "rb") as file:
		print dump_record_info(file)
		print dump_exth(file)
		file.seek(0)
		with open(fname + ".html", "w") as out:
			for skip in xrange(100):
				data = dump_html(file, skip=skip)
				if len(data) > 0:
					out.write(data)
					out.write(b'\n\n<!-- End of Book -->\n\n')
				else:
					break
	