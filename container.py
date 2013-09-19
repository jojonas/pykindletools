class NotFinishedError(Exception):
	pass
	
class FinishedError(Exception):
	pass
	
class SerializedContainer(object):
	def __init__(self):
		self.serialized = None
		
	def finish(self):
		if self.serialized is None:
			self.serialized = self.serialize()
		
	def serialize(self):
		raise NotImplementedError("serialize() is missing.")
		return ""
	
	def length(self):
		if self.serialized is None:
			raise NotFinishedError()
		else:
			return len(self.serialized)
			
	def data(self):
		if self.serialized is None:
			raise NotFinishedError()
		else:
			return self.serialized
			
	def __setattr__(self, name, value):
		if name == 'serialized' or  self.serialized is None:
			super(SerializedContainer, self).__setattr__(name, value)
		else:
			raise FinishedError("Can not set '%s', object is already finished." % name)
		
		