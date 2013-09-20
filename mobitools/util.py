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
		