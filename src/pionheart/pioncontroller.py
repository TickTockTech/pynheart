import curses
import time

from boardgame.controller import Controller
from boardgame.board import Board
from .pionboard import PionBoard

'''
PionController


'''

class PionController(Controller):

    SET_UP_BOARD = 2
    MOVE_PIECE_MODE = 1
    MENU_MODE = 0

    def __init__(self, controllable, board):
        super(PionController, self).__init__(controllable)

        self.mode = PionController.MOVE_PIECE_MODE
        self.board = board
        self.cursor = {
            "x": 0,
            "y": 0
        }

    def getCursor(self):
        return self.cursor["x"], self.cursor["y"]

    def left(self):
        if self.cursor["x"] > 0:
            self.cursor["x"] -= 1
            self.msg = "Left"

    def right(self):
        if self.cursor["x"] < self.board.width - 1:
            self.cursor["x"] += 1
            self.msg = "Right"

    def up(self):
        if self.cursor["y"] > 0:
            self.cursor["y"] -= 1
            self.msg = "Up"

    def down(self):
        if self.cursor["y"] < self.board.height - 1:
            self.cursor["y"] += 1
            self.msg = "Down"
