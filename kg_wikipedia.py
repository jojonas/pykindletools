import pykindle.webapis

import argparse

parser = argparse.ArgumentParser(description="Create a MOBI file from a wikipedia article.")
parser.add_argument('title', help="Wikipedia search term")
parser.add_argument('-l, --language', help="Wikipedia language", default="en", dest='lang')
parser.add_argument('-k, --kindlegen', metavar='EXE', help="location of kindlegen.exe", default="kindlegen.exe", dest='kindlegen')

args = parser.parse_args()

book = pykindle.webapis.wikipedia.WikipediaArticleBook(args.title)
book.setKindlegen(args.kindlegen)
book.setLanguage(args.lang)
book.gather()
book.createMobi()
	