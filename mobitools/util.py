import struct
import collections

def variable_width_int_backwards(value):
	bytes = []
	if value == 0:
		bytes.append(0b10000000)
	else:
		while value != 0:
			bytes.append(value & 0b01111111)
			value = value >> 7
		bytes[-1] |= 0b10000000
	
	return "".join(map(chr, reversed(bytes)))
		

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
	infos['string'] 			=  lambda d: "'%s'" % d
	infos['hex'] 				=  lambda d: tuple("%2x" % ord(c) for c in d)
	infos['dec'] 				=  lambda d: tuple(ord(c) for c in d)
	infos['char'] 				=  lambda d: unpack_multi('c', d)
	infos['signed char'] 		=  lambda d: unpack_multi('b', d)
	infos['unsigned char']	 	=  lambda d: unpack_multi('B', d)
	infos['bool'] 				=  lambda d: unpack_multi('?', d)
	infos['short'] 				=  lambda d: unpack_multi('h', d)
	infos['unsigned short']		=  lambda d: unpack_multi('H', d)
	infos['int'] 				=  lambda d: unpack_multi('I', d)
	infos['long'] 				=  lambda d: unpack_multi('l', d)
	infos['unsigned long'] 		=  lambda d: unpack_multi('L', d)
	infos['long long'] 			=  lambda d: unpack_multi('q', d)
	infos['unsigned long long'] =  lambda d: unpack_multi('Q', d)
	infos['float'] 				=  lambda d: unpack_multi('f', d)
	infos['double'] 			=  lambda d: unpack_multi('d', d)

	retval = ''
	for key, value in infos.iteritems():
		try:
			retval += "{:20}:   {}\n".format(key, str(value(data)))
		except RuntimeError:
			pass
	return retval