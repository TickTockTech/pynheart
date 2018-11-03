class Game(object):

	def __init__(self, board):
		self.running = True
		self.board = board

	def quit(self):
		self.running = False
		