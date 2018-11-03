import curses
import time

from .pioncontroller import PionController
from gamelog import Log

class PionTextController(PionController):
    def __init__(self, controllable, board):
        super(PionTextController, self).__init__(controllable, board)

        self.commands = [
            "D",        # Down
            "U",        # Up
            "R",        # Right
            "L",        # Left
            "C 4,4",    # Cursort to 4,4
            "A",        # Select
            "S",        # Skip
            "Q"         # Quit
        ]
        self.ix = 0
    
    def setCommandChain(self, cmds):
        self.commands = cmds

    def getInput(self):
        time.sleep(4)

        if self.ix < len(self.commands):
            cmd_line = self.commands[self.ix]
            self.ix += 1

            splitz = cmd_line.split(" ", 1)

            cmd = splitz[0].upper()
            param = None

            if len(splitz) > 1:
                param = splitz[1]

            Log.info("Command -> {}".format(cmd_line, cmd))

            if cmd == "Q":
                self.controllable.quit()
            elif cmd == "L":
                self.controllable.left()
            elif cmd == "R":
                self.controllable.right()
            elif cmd == "D":
                self.controllable.down()
            elif cmd == "U":
                self.controllable.up()
            elif cmd == "C":
                if param == None:
                    raise GameCommandFormatException("No parameters for C (cursor) command.")
                coords = param.split(',')
                if len(coords) != 2:
                    raise GameCommandFormatException("Invalid param for C (cursor) command - should be x,y")
                self.cursor["x"] = int(coords[0])
                self.cursor["y"] = int(coords[1])
            elif cmd == "A":
                self.controllable.select(self.cursor["x"], self.cursor["y"])
            elif cmd == "S":
                self.controllable.skip()
