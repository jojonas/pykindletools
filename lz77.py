import io

def lz77_compress(data):
	output = ""
	
	position = 0
	space = False
	
	start_pos = 0
	while position < len(data):
		overlap_length = 0
		
		if start_pos < position - 2047: #window size maximum 2047 (11 bits)
			start_pos = position - 2047
		
		result = start_pos
		for i in range(3, min(len(data) - position, 10)+1):
			pattern = data[position:position+i]
			result = data.find(pattern, result, position)
			if result == -1:
				break
			last_good_start = result
			overlap_length = i-1
			
		if overlap_length >= 3:
			overlap_distance = position - last_good_start
			byte = (overlap_distance << 3) | (overlap_length-3)
			if space:
				output += ' '
				space = False
			output += chr(0x80 | (byte >> 8))
			output += chr(byte & 0xff)
			position += overlap_length
		else:
			char = ord(data[position])
			position += 1
			
			if space and 0xc0 <= (char^0x80) <= 0xff:
				output += chr(char ^ 0x80)
				space = False
				
			elif not space and char == 32:
				space = True
				
			else:
				if space:
					output += ' '
					space = False
					
				if char == 0 or 0x09 <= char <= 0x7f:
					output += chr(char)
				else:
					output += chr(1)
					output += chr(char)
				
				
	if space:
		output += ' '
		
	return output
	
def lz77_decompress(stream, maxOut=4096):
	if isinstance(stream, str):
		stream = io.BytesIO(stream)
		
	output = ""
	while len(output) < maxOut:
		raw = stream.read(1)
		if len(raw) == 0:
			break # EOF
		char = ord(raw)
		if char == 0 or 0x09 <= char <= 0x7f:
			output += chr(char)
		elif 0x01 <= char <= 0x08:
			output += stream.read(char)
		elif 0x80 <= char <= 0xbf:
			nextChar = ord(stream.read(1))
			pair = (char << 8) | nextChar
			distance = (pair & 0b0011111111111000) >> 3
			length = (pair   & 0b0000000000000111)
			length += 3
			toAppend = ''
			for pos in xrange(min(length, maxOut-len(output))):
				toAppend += output[-distance+pos]
			output += toAppend
		elif 0xc0 <= char <= 0xff:
			output += ' '
			output += chr(char ^ 0x80)
	return output
	