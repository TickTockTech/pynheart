import os
import curses
import time

from boardgame.renderer import Renderer
from boardgame.boarderrors import *
from boardgame.board import Board
from .piongame import PionGame
from .pionboard import PionBoard
from .pionpiece import PionPiece
from .pioncursespopup import PionCursesPopup
from gamelog import Log

class PionCursesRenderer(Renderer):
    y_os = 2

    def __init__(self, game, controller):
        super(PionCursesRenderer, self).__init__(game)

        self.controller = controller
        self.render_skew = Renderer.ATTACK_SKEW

    def init(self, stdscr):
        if hasattr(self.__class__ , "stdscr"):
            raise MultipleRenderersError("Only one renderer allowed.")

        self.__class__.stdscr = stdscr
        
        curses.cbreak()
        curses.noecho()

        PionCursesRenderer.initColours()
    
    def render(self):
        stdscr = self.__class__.stdscr

        stdscr.clear()
        
        maxy, maxx = stdscr.getmaxyx()
    
        width = self.board.width
        height = self.board.height

        Log.info("Draw board {} x {}".format(maxx, maxy))
        stdscr.clear()

        stdscr.addstr(0, 0, "Press 'q' to Quit.")

        if self.game.main_state == PionGame.GAME_STATE_PHASE_1:
            stdscr.addstr(1, 30, "Press 's' to Start.")

        stdscr.addstr(0, 30, "{}".format(self.game.getSubStateStr()))

        # Show any messages in response to user actions
        msg, lvl = self.game.consumeFeedback()
        if lvl >= 0 and msg != None:
            stdscr.addstr(1, 30, "> {} ({})".format(msg, lvl))
            if lvl > 1:
                PionCursesRenderer.beep()

        stdscr.addstr(2, 30, ":{}".format(self.controller.debugMsg()))

        # Render the board
        board_col = curses.color_pair(64)
        for y in range(0, height * 2, 2):
            stdscr.addstr(y + self.y_os, 0, "+", board_col)
            stdscr.addstr(y + self.y_os + 1, 0, "|", board_col)
            for x in range(0, width * 2, 2):
                stdscr.addstr(y + self.y_os, x + 1, "-+", board_col)
                stdscr.addstr(y + self.y_os + 1, x + 2, "|", board_col)

        bot = (height * 2) + self.y_os
        stdscr.addstr(bot, 0, "+", board_col)
        for x in range(0, width * 2, 2):
            stdscr.addstr(bot, x + 1, "-+", board_col)

        defend_col = curses.color_pair(32)
        attack_col = curses.color_pair(216)

        cX, cY = self.controller.getCursor()

        # Render the pieces that are on the board
        for y in range(0, height):
            for x in range(0, width):
                piece = self.board.grid[(x,y)]

                if piece != Board._Empty:
                    defender = piece.getAttrib("defender")
                    if defender:
                        piece_col = defend_col
                    else:
                        piece_col = attack_col

                    char = piece.getAttrib("console_chr")

                    # In phase 2 of the game we should hide the opponents pieces.
                    if not self.game.main_state == PionGame.GAME_STATE_PHASE_1:
                        if not piece.getAttrib("entry_point") and not piece.getAttrib("revealed"):
                            if self.render_skew == Renderer.ATTACK_SKEW and defender:
                                char = "X"
                            elif self.render_skew == Renderer.DEFENCE_SKEW and not defender:
                                char = "X"

                    if cX == x and cY == y:
                        PionCursesRenderer.pieceRender(stdscr, x, y, char, curses.A_REVERSE)
                    else:
                        PionCursesRenderer.pieceRender(stdscr, x, y, char, piece_col)
                else:
                    if cX == x and cY == y:
                        PionCursesRenderer.pieceRender(stdscr, x, y, " ", curses.A_REVERSE)

        # Shift the cursor out of the way <- Must be some way to hide it!!!
        stdscr.addstr(maxy - 1, maxx - 1, '')

        if self.game.main_state == PionGame.GAME_STATE_PHASE_1:
            if self.game.sub_state == PionGame.P1_SELECT_SPAWN_PIECE:
                # TODO: Shift this into the Game class as it is game logic.
                defenders = PionPiece.getDefenders()
                names = []
                for piece in defenders:
                    names.append(piece["name"])
                names.append("Quit")
                popup = PionCursesPopup(stdscr)
                result = popup.show("Select piece: ", names)
                Log.info("Piece selected: {}".format(names[result]))
                self.game.sub_state = PionGame.P1_SELECT_SPAWN_LOCATION
                popup.close()

                if result != -1:
                    piece = PionPiece.getPiece(defenders[result]["key"], (cX, cY))
                    self.board.addPiece(piece)

                self.render()

        if self.game.main_state == PionGame.GAME_STATE_PHASE_2:
            if self.game.sub_state == PionGame.P2_SELECT_SPAWN_PIECE:
                # TODO: Shift this into the Game class as it is game logic.
                attackers = PionPiece.getAttackers()
                names = []
                for piece in attackers:
                    names.append(piece["name"])
                names.append("Quit")
                popup = PionCursesPopup(stdscr)
                result = popup.show("Select piece: ", names)
                if result != -1:
                    Log.info("Piece selected: {} -> {}".format(names[result], attackers[result]["key"]))
                    piece = PionPiece.getPiece(attackers[result]["key"], (cX, cY))
                    spawner = self.board.removePieceAt( (cX,cY) )
                    self.board.addPiece(piece)
                    # Attach the spawner to the piece as we're on top of it.
                    piece.setAttrib("spawner", spawner)
                    Log.info("Render: Attach {} to {}.".format(spawner.getAttrib("name"), piece.getAttrib("name")))
                    self.game.selected_piece = piece
                    self.game.sub_state = PionGame.P2_MOVE_ATTACKING_PIECE
                else:
                    self.game.sub_state = PionGame.P2_SELECT_ATTACKING_PIECE
                popup.close()
                self.render()

        stdscr.refresh()

    @classmethod
    def pieceRender(cls, stdscr, x, y, char, col):
        stdscr.addstr((y * 2) + cls.y_os + 1, (x * 2) + 1, char, col)

    @staticmethod
    def beep():
        print "\a"

    @staticmethod
    def initColours():
        curses.start_color()
        curses.use_default_colors()

        if os.name == "nt":
            return

        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        print '[PionCurses] {0} colors available'.format(curses.COLORS)


