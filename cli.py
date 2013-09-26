import argparse
import inspect

TYPES = {
	"int": int,
	"string": str,
	"str": str,
	"float": float,
	"double": float,
	"boolean": bool
}

def make_argparser(BookClass):
	args, _, _, defaults = inspect.getargspec(BookClass.__init__)
	args.remove('self')
	doclines = BookClass.__doc__.split("\n")
	nrequired = len(args) - (len(defaults) if defaults is not None else 0)
	arginfos = []
	
	for i, arg in enumerate(args):
		arginfo = dict()
		
		arginfo['name'] = arg
		
		for j, line in enumerate(doclines):
			line = line.strip()
			pattern = ":param {arg}:".format(arg=arg)
			if line.startswith(pattern):
				arginfo['help'] = line[len(pattern):]
				line = doclines[j+1].strip()
				pattern = ":type"
				if line.startswith(pattern):
					arginfo['type'] = TYPES[line[len(pattern):].strip()]
				break
			
		if i >= nrequired:
			arginfo['default'] = defaults[i-nrequired]
			arginfo['name'] = "--" + arginfo['name']
	
		arginfos.append(arginfo)
		
	help = ''
	for docline in doclines:
		if docline.strip() == '':
			break
		else:
			help += docline + " "
		
	parser = argparse.ArgumentParser(description=help)
	for arginfo in arginfos:
		name = arginfo['name']
		del arginfo['name']
		if 'default' in arginfo and 'help' in arginfo:
			arginfo['help'] += " (default: {d})".format(d=arginfo['default'])
		parser.add_argument(name, **arginfo)
	
	return parser
	
def construct_with_namespace(BookClass, namespace):
	args, _, _, _ = inspect.getargspec(BookClass.__init__)
	args.remove('self')
	
	arguments = {}
	for arg in args:
		try:
			value = vars(namespace)[arg]
			arguments[arg] = value
		except KeyError:
			pass
			
	return BookClass(**arguments)
	
def cli(BookClass):
	parser = make_argparser(BookClass)
	parser.add_argument(
		'-k, --kindlegen', 
		metavar='EXECUTABLE', 
		help="location of kindlegen executalbe", 
		default="kindlegen", 
		dest='kindlegen'
	)
	
	namespace = parser.parse_args()
	
	book = construct_with_namespace(BookClass, namespace)
	book.setKindlegen(namespace.kindlegen)
	book.gather()
	book.createMobi()

	