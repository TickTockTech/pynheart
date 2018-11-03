class Renderer(object):

    ATTACK_SKEW = 0
    DEFENCE_SKEW = 1

    def __init__(self, game):
		self.game = game
		self.board = game.board

    def render(self):
		raise NotImplementedError("BoardRenderer sub-classes must implement a render method.")