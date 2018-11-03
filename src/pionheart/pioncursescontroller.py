import curses
import time

from .pioncontroller import PionController

class PionCursesController(PionController):
    def __init__(self, controllable, board):
        super(PionCursesController, self).__init__(controllable, board)
    
    def hookUp(self, stdscr):
        self.stdscr = stdscr

    def getInput(self):
        stdscr = self.stdscr
        
        # Blocks
        c = stdscr.getch()

        if c == ord('q'):
            self.controllable.quit()
        elif c == curses.KEY_LEFT:
            self.left()
        elif c == curses.KEY_RIGHT:
            self.right()
        elif c == curses.KEY_UP:
            self.up()
        elif c == curses.KEY_DOWN:
            self.down()
        elif c == ord(' ') or c == curses.KEY_ENTER or c == ord('\n'):
            self.controllable.select(self.cursor["x"], self.cursor["y"])
        elif c == ord('s'):
            self.controllable.skip()
