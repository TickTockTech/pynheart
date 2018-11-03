from copy import deepcopy

class Piece(object):

	def __init__(self, attr = {}, location = None):

		assert isinstance(attr, object)
		assert isinstance(location, tuple)
		assert len(location) == 2

		self.attr = deepcopy(attr)
		self.location = location

	def getLocation(self):
		return self.location

	def getAttribs(self):
		return self.attr

	def setAttrib(self, key, value):
		self.attr[key] = value

	def getAttrib(self, key, default = None):
		if key in self.attr:
			return self.attr[key]
		return default
