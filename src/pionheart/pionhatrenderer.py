try:
    from sense_hat import SenseHat
except:
    pass

from boardgame.renderer import Renderer
from boardgame.game import Game
from boardgame.board import Board
from .pionboard import PionBoard
from gamelog import Log

class PionHatRenderer(Renderer):

    def __init__(self, game, controller):
        self.game = game
        self.board = game.board
        self.controller = controller
        self.sense = SenseHat()

        orientation = self.sense.get_orientation_degrees()
        pitch = (int)(((orientation["pitch"] + 45) / 90) % 4)
        Log.info("PiHAT: pitch {}".format(pitch))
        pitch_correction = [180, 90, 0, 270]
        self.sense.rotation = pitch_correction[pitch]

        self.sense.rotation = pitch_correction[pitch]

    def render(self):
        cX, cY = self.controller.getCursor()

        for x in range(0, 8):
            for y in range(0, 8):
                r = g = b = 0

                square = self.board.get((x,y))
                if square != None and not square == "":
                    col = square.getAttrib("pihat_col")
                    r = col["r"]
                    g = col["g"]
                    b = col["b"]
                else:
                    col = {"r":0,"g":0,"b":0}

                if x == cX and y == cY:
                    r += 95
                    g += 95
                    b += 95

                self.sense.set_pixel(x, y, r, g, b)
