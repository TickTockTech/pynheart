import curses
import time

from .pioncontroller import PionController
from gamelog import Log

class PionAIController(PionController):
    def __init__(self, controllable, board):
        super(PionAIController, self).__init__(controllable, board)

    def getInput(self):
        time.sleep(2)

        self.controllable.skip()
