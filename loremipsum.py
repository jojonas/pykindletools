from mobitools import Book
		
if __name__=="__main__":
	book = Book()
	book.title = "Lorem Ipsum"
	book.author = "Max Mustermann"
	book.publisher = "My Verlag"
	
	import re
	with open("loremipsum.txt", "r") as input:
		data = input.read()
		clean = re.sub(">\s*<","><", data)
		book.addText(clean)
		
	with open("loremipsum.mobi", "wb") as file:
		book.write(file)