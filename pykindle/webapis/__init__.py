import importlib
import sys
import os, os.path

PREFIX = 'module_'

currentDir = os.path.dirname(os.path.realpath(__file__))

loaded = {}
for fname in os.listdir(currentDir):
	fullfname = os.path.join(currentDir, fname)
	if os.path.isfile(fullfname):
		moduleName, ext = os.path.splitext(fname)
		if fname.startswith(PREFIX) and ext.lower() in ['.pyc', '.py']:
			moduleName = moduleName[len(PREFIX):]
			if not moduleName in loaded:
				fullName = "{pkg}.{name}".format(pkg=__name__, name=moduleName)
				realName = ".module_{name}".format(name=moduleName)
				try:
					loaded[moduleName] = sys.modules[fullName] = importlib.import_module(
						realName, 
						package=__name__
					)
				except ImportError as e:
					print "Module '{name}' will be unavailable:".format(name=moduleName), e
				
				
globals().update(loaded)
		