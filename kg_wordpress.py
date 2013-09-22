import pykindle.webapis

import getpass
import argparse

parser = argparse.ArgumentParser(description="Create a MOBI file from a wordpress site.")
parser.add_argument('url', help="URL of the XML-RPC service")
parser.add_argument('username', help="log in username")
parser.add_argument('-k, --kindlegen', metavar='EXE', help="location of kindlegen.exe", default="kindlegen.exe", dest='kindlegen')

args = parser.parse_args()

password = getpass.getpass("Enter password for user '{user}': ".format(user=args.username))

book = pykindle.webapis.wordpress.WordpressBook(args.url, args.username, password)
book.setKindlegen(args.kindlegen)
book.gather()
book.createMobi()
	