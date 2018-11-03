class Controllable(object):
    '''
    Controllable - a class which takes some form of input from a controller. This could be a keyboard, mouse, touch, network, file, etc...
    '''

    def select(self, x, y):
        raise NotImplementedError("Controllable must implement select x,y function")

    def quit(self):
        raise NotImplementedError("Controllable must implement quit function")

    def skip(self):
        raise NotImplementedError("Controllable must implement skip function")

    def start(self):
        raise NotImplementedError("Controllable must implement start function")

    def up(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def right(self):
        pass