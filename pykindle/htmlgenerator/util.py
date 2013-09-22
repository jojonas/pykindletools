import re
import subprocess
import os

def call_kindlegen(kindlegen, fname):
	with open(os.devnull, "w") as FNULL:
		subprocess.call([kindlegen, fname], stdout=FNULL, stderr=subprocess.STDOUT)
	
def make_filename(title):
	title = title.strip().lower().replace(' ', '_')[:32]
	fname = re.sub(r'[^a-zA-Z0-9_]', '', title)
	return fname
