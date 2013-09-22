import pykindle.webapis

import argparse

parser = argparse.ArgumentParser(description="Create a MOBI file from a rss feed.")
parser.add_argument('url', help="URL of the RSS feed")
parser.add_argument('-k, --kindlegen', metavar='EXE', help="location of kindlegen.exe", default="kindlegen.exe", dest='kindlegen')

args = parser.parse_args()

book = pykindle.webapis.rss.RSSBook(args.url)
book.setKindlegen(args.kindlegen)
book.gather()
book.createMobi()
	