# -*- coding: utf-8 -*-

import json
import math

from boardgame.piece import Piece
from boardgame.boarderrors import MovementAllowanceExceeded, NoMoveError, PieceNotFoundError
from gamelog import Log

class PionPiece(Piece):

	PIHAT_RGB_BLUE = {"r":0,"g":0,"b":255}
	PIHAT_RGB_GREEN = {"r":0,"g":255,"b":0}
	PIHAT_RGB_CYAN = {"r":0,"g":255,"b":255}
	PIHAT_RGB_RED = {"r":255,"g":0,"b":0}
	PIHAT_RGB_PURPLE = {"r":255,"g":0,"b":255}
	PIHAT_RGB_YELLOW = {"r":255,"g":255,"b":0}
	PIHAT_RGB_WHITE = {"r":255,"g":255,"b":255}

	PIHAT_RGB_BLUE_D = {"r":0,"g":0,"b":127}
	PIHAT_RGB_GREEN_D = {"r":0,"g":127,"b":0}
	PIHAT_RGB_CYAN_D = {"r":0,"g":127,"b":127}
	PIHAT_RGB_RED_D = {"r":127,"g":0,"b":0}
	PIHAT_RGB_PURPLE_D = {"r":127,"g":0,"b":127}
	PIHAT_RGB_YELLOW_D = {"r":127,"g":127,"b":0}
	PIHAT_RGB_WHITE_D = {"r":127,"g":127,"b":127}

	def __init__(self, attr, location = None):
		super(PionPiece, self).__init__(attr, location)

	def _move(self, tuple_loc):
		assert isinstance(tuple_loc, tuple)
		assert len(tuple_loc) == 2

		current_x = self.location[0]
		current_y = self.location[1]

		new_x = tuple_loc[0]
		new_y = tuple_loc[1]

		dx = abs(current_x - new_x)
		dy = abs(current_y - new_y)
		moves = math.sqrt( (dx * dx) + (dy * dy) )

		if moves == 0:
			Log.warn("Attempt to move from {} to {} which isn't a move.".format(self.location, tuple_loc))
			raise NoMoveError("Attempt to move from {} to {} which isn't a move.".format(self.location, tuple_loc))

		moves_allowed = self.getAttrib("moves", 0)

		if moves > moves_allowed:
			Log.warn("Attempt to move from {} to {}. Moves {} more than {} allowed.".format(self.location, tuple_loc, moves, moves_allowed))
			raise MovementAllowanceExceeded("Attempt to move from {} to {}. Moves {} more than {} allowed.".format(self.location, tuple_loc, moves, moves_allowed))

		self.location = tuple_loc

# *****************************************************************************
# DEFENDERS
# *****************************************************************************
	@classmethod
	def loadPieces(cls, filename):
		Log.info("Load pieces from: {}".format(filename))

		cls._defenders = []
		cls._attackers = []

		with open(filename, 'r') as pFile:
			piece_data = pFile.read()
			cls._pieces = json.loads(piece_data)
			cls._pieceKeys = []
			Log.info("    OK: {}".format(filename))

			for key, value in cls._pieces.iteritems():
				cls._pieces[key]["key"] = key
				cls._pieceKeys.append(key)
				if cls._pieces[key]["defender"]:
					cls._defenders.append(cls._pieces[key])
				else:
					cls._attackers.append(cls._pieces[key])

	@classmethod
	def getAttackers(cls):
		return cls._attackers

	@classmethod
	def getDefenders(cls):
		return cls._defenders

	@classmethod
	def getPieceData(cls, name):
		return cls._pieces[name]

	@classmethod
	def getPiece(cls, name, loc = None):
		if not name in cls._pieces:
			raise PieceNotFoundError("Cannot find {} in piece data.".format(name))

		return PionPiece(cls._pieces[name], loc)
