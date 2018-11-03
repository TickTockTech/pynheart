import curses

from gamelog import Log

class PionCursesPopup:
    def __init__(self, stdscr):
        self.stdscr = stdscr

    def _createWin(self):
        x = 30
        y = 5
        maxy, maxx = self.stdscr.getmaxyx()
        width = maxx - x - 1
        height = len(self.menu) + 4

        self.stdscr.refresh()
        self.popup = self.stdscr.subwin(height, width, y, x)
        self.popup.keypad(1)

    def _fillWin(self, chr):
        y, x = self.popup.getmaxyx()
        s = chr * (x - 1)
        for l in range(y):
            self.popup.addstr(l, 0, s)

    def _drawWin(self):
        self.popup.clear()
        self.popup.addstr(1, 1, self.title)

        y = 3
        for item in self.menu:
            self.popup.addstr(y, 3, item)
            y += 1

        self.popup.addstr(3 + self.ix, 1, '')

        self.popup.refresh()

    def show(self, title, menu):
        self.ix = 0
        self.title = title
        self.menu = menu

        self._createWin()

        # self.fillwin(".")

        while True:
            self._drawWin()
            c = self.popup.getch()
            Log.info("IX:" + str(self.ix) + "/" + str(len(self.menu) - 1) + " " + str(c) + " " + str(curses.KEY_UP))
            if c == curses.KEY_UP:
                Log.info("up")
                if self.ix > 0:
                    self.ix -= 1
            elif c == curses.KEY_DOWN:
                Log.info("dwn")
                if self.ix < len(menu) - 1:
                    self.ix += 1
            elif c == ord(' ') or c == curses.KEY_ENTER or c == ord('\n'):
                return self.ix
            elif c == ord('q'):
                return -1

    def close(self):
        del self.popup

        self.stdscr.touchwin()
        self.stdscr.refresh()