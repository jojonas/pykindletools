import io
	
def lz77_compress(data, compress8=True):
	output = io.BytesIO()
	
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
			overlap_length = i
			
		if overlap_length >= 3:
			overlap_distance = position - last_good_start
			byte = (overlap_distance << 3) | (overlap_length-3)
			if space:
				output.write(' ')
				space = False
			output.write(chr(0x80 | (byte >> 8)))
			output.write(chr(byte & 0xff))
			position += overlap_length
		else:
			char = ord(data[position])
			position += 1
			
			if space and 0xc0 <= (char^0x80) <= 0xff:
				output.write(chr(char ^ 0x80))
				space = False
				
			elif not space and char == 32:
				space = True
				
			else:
				if space:
					output.write(' ')
					space = False
					
				if char == 0 or 0x09 <= char <= 0x7f:
					output.write(chr(char))
				else:
					output.write(chr(1))
					output.write(chr(char))
				
	if space:
		output.write(' ')
		
	if compress8:
		MAX_ACC = 8
		
		clean = io.BytesIO()
		output.seek(0,2)
		end = output.tell()
		output.seek(0)
		accumulator = b''
		while output.tell() < end:
			char = ord(output.read(1))
			if 0x01 <= char <= MAX_ACC: 
				accumulator += output.read(char)
				while len(accumulator) > MAX_ACC:
					clean.write(chr(MAX_ACC))
					clean.write(accumulator[:MAX_ACC])
					accumulator = accumulator[MAX_ACC:]
			else:
				if len(accumulator) > 0:
					assert len(accumulator) <= MAX_ACC
					clean.write(chr(len(accumulator)))
					clean.write(accumulator)
					accumulator = b''
					
				clean.write(chr(char))
				
				if 0x80 <= char <= 0xbf:
					clean.write(output.read(1))
			
		return clean.getvalue()
	else:
		return output.getvalue()
		
def lz77_decompress(stream, maxOut=None):
	if isinstance(stream, str):
		stream = io.BytesIO(stream)
		
	output = ""
	while maxOut is None or len(output) < maxOut:
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
			
			if maxOut is None:
				for pos in xrange(length):
					toAppend += output[-distance+pos]
			else:
				for pos in xrange(min(length, maxOut-len(output))):
					toAppend += output[-distance+pos]
					
			output += toAppend
		elif 0xc0 <= char <= 0xff:
			output += ' '
			output += chr(char ^ 0x80)
	return output
	