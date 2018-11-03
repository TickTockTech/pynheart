import json

from boardgame.board import Board
from .pionpiece import *

class PionBoard(Board):

	@staticmethod
	def load(filename):
		with open(filename, 'r') as f:
			string = f.read()

			return PionBoard.fromJsonString(string)

		raise FileNotFoundError("Cannot find {}".format(filename))

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write( self.toJsonString() )

	def toString(self):
		result = "+" + ("-+" * self.width) + "\n"
		for y in range(self.height):
			line = "|"
			for x in range(self.width):
				loc = (x, y)

				square = self.grid[loc]

				if square != Board._Empty:
					char = square.getAttrib("console_chr")
				else:
					char = " "

				line += char + "|"
			result += line + "\n"

			result += "+" + ("-+" * self.width) + "\n"

		return result

	def toJsonString(self):
		json_compat = {}
		for row in range(0, self.width):
			for col in range(0, self.height):
				key = "(" + str(row) + "," + str(col) + ")"
				loc = (row,col)
				square = self.grid[loc]
				if square != Board._Empty:
					json_compat[key] = square.getAttrib("key")
				else:
					json_compat[key] = None

		save_data = {
			"width": self.width,
			"height": self.height,
			"board": json_compat
		}
		return json.dumps(save_data, indent=2, sort_keys=True)

	@staticmethod
	def fromJsonString(json_str):
		obj_data = json.loads(json_str)

		width = obj_data["width"]
		height = obj_data["height"]

		new_board = PionBoard(width, height)

		board = obj_data["board"]
		for row in range(0, width):
			for col in range(0, height):
				key = "(" + str(row) + "," + str(col) + ")"
				square = board[key]
				loc = (row,col)
				if square != None:
					piece = PionPiece.getPiece(square, loc)
					new_board.grid[loc] = piece
				else:
					new_board.grid[loc] = Board._Empty

		return new_board
