class Controller(object):
    '''
    Controller - This takes input from an input device, a file, the network, and converts it into game input.
    '''
    def __init__(self, controllable):
        self.controllable = controllable
        self.msg = ""

    def getInput(self):
        raise NotImplementedError("BoardController sub-classes must implement a getInput method.")

    def debugMsg(self):
        return self.msg

    def attach(self, controllable):
        self.controllable = controllable
