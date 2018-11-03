from .boarderrors import *

from gamelog import Log

class Board:
	_Empty = ""

	def __init__(self, width, height):

		assert isinstance(width, int)
		assert isinstance(height, int)
		assert width > 0
		assert height > 0

		self.width = width
		self.height = height

		self.grid = {}

		for row in range(self.width):
			for col in range(self.height):
				self.grid[(row,col)] = self.__class__._Empty

	def get(self, grid_tuple):
		if grid_tuple in self.grid:
			result = self.grid[grid_tuple]
			return result

		return None

	def set(self, grid_tuple, value):
		if not grid_tuple in self.grid:
			Log.warn("{} is not on the {} x {} grid.".format(grid_tuple, self.width, self.height))
			raise IndexError("{} is not on the {} x {} grid.".format(grid_tuple, self.width, self.height))

		self.grid[grid_tuple] = value

	def addPieces(self, pieces):
		for piece in pieces:
			loc = piece.getLocation()
			if not loc in self.grid:
				Log.warn("Piece at {} is not on the {} x {} grid.".format(loc, self.width, self.height))
				raise IndexError("Piece at {} is not on the {} x {} grid.".format(loc, self.width, self.height))
			if self.grid[loc] != self.__class__._Empty:
				Log.warn("Square {} already has something on.".format(loc))
				raise SquareNotEmpty("Square {} already has something on.".format(loc))
			self.grid[loc] = piece

	def addPiece(self, piece):
		loc = piece.getLocation()
		if not loc in self.grid:
			raise IndexError("Piece at {} is not on the {} x {} grid.".format(loc, self.width, self.height))
		if self.grid[loc] != self.__class__._Empty:
			Log.warn("Square {} already has something on.".format(loc))
			raise SquareNotEmpty("Square {} already has something on.".format(loc))
		self.grid[loc] = piece

	def findPiece(self, piece):
		for row in range(0, self.width):
			for col in range(0, self.height):
				loc = (row,col)
				if piece is self.grid[loc]:
					return loc

		return None

	def removePiece(self, piece):
		loc = self.findPiece(piece)

		if loc == None:
			raise PieceNotFoundError("Couldn't find {}".format(piece.getAttrib("name")))

		self.grid[loc] = Board._Empty

	def removePieceAt(self, loc):
		piece = self.grid[loc]
		self.grid[loc] = Board._Empty
		return piece

	def movePiece(self, piece, loc):
		old_loc = self.findPiece(piece)

		try:
			piece._move(loc)

			self.grid[old_loc] = Board._Empty
			self.grid[loc] = piece
			Log.info("Board - moved {} from {} -> {}".format(piece.getAttrib("name"), old_loc, loc))
		except:
			Log.warn("Cannot move {} from {} to {}".format(piece.getAttrib("name"), old_loc, loc))
			raise MoveFailedError("Cannot move {} from {} to {}".format(piece.getAttrib("name"), old_loc, loc))
