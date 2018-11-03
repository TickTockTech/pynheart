import curses
import time

from .pioncontroller import PionController
from gamelog import Log

class PionNetworkController(PionController):
    def __init__(self, controllable, board):
        super(PionNetworkController, self).__init__(controllable, board)
    
    def getInput(self):
        time.sleep(2)

        self.controllable.skip()
