import sys
from collections import namedtuple

from boardgame.board import Board
from boardgame.boarderrors import *
from boardgame.game import Game
from boardgame.controllable import Controllable

from gamelog import Log

class PionGame(Game, Controllable):
    '''
    The state and rules of the Pi 'n Heart game.
    '''

    GAME_STATE_PHASE_1 = 0
    GAME_STATE_PHASE_2 = 1

    P1_NOT_APPLICABLE = -1
    P1_SELECT_SPAWN_LOCATION = 0
    P1_SELECT_SPAWN_PIECE = 1

    P2_NOT_APPLICABLE = -1
    P2_SELECT_DEFENDING_PIECE = 0
    P2_SELECT_ATTACKING_PIECE = 1
    P2_SELECT_SPAWN_PIECE = 2
    P2_MOVE_DEFENDING_PIECE = 3
    P2_MOVE_ATTACKING_PIECE = 4

    ATTACK_ROUND = 0
    DEFENCE_ROUND = 1

    FeedbackMsg = namedtuple('FeedbackMsg', 'msg lvl')

    INFO = 0
    WARN = 1
    ERR = 2

    NO_MSG = FeedbackMsg(None, -1)

    P1_State_str = [
        "Select spawn location",
        "Chose type"
    ]

    P2_State_str = [
        "Select defender",
        "Select attacker",
        "Spawn attacker",
        "Move defender [{}]",
        "Move attacker [{}]",
    ]

    def __init__(self, board):
        super(PionGame, self).__init__(board)
        
        self.main_state = PionGame.GAME_STATE_PHASE_1
        self.sub_state = PionGame.P1_SELECT_SPAWN_LOCATION # P2_SELECT_ATTACKING_PIECE
        self.message = PionGame.NO_MSG

    def select(self, x, y):
        Phase1_Funcs = [
            self.phase1_select,
            self.phase1_spawn
        ]
        Phase2_Funcs = [
            self.phase2_select,
            self.phase2_select,
            self.phase2_choose,
            self.phase2_place,
            self.phase2_place,
        ]

        if self.main_state == PionGame.GAME_STATE_PHASE_1:
            Phase1_Funcs[self.sub_state](x, y)
        else:
            Phase2_Funcs[self.sub_state](x, y)

    def phase1_select(self, x, y):
        if self.sub_state == PionGame.P1_SELECT_SPAWN_LOCATION:
            self.sub_state = PionGame.P1_SELECT_SPAWN_PIECE

    def phase1_spawn(self, x, y):
        Log.info("Spawn!")

    def phase2_select(self, x, y):
        loc = (x, y)
        square = self.board.get(loc)

        if square == Board._Empty:
            self.feedback("Square empty", PionGame.ERR)
        else:
            assert loc == square.getLocation()
            defender = square.getAttrib("defender")
            if self.sub_state == PionGame.P2_SELECT_ATTACKING_PIECE:
                if defender:
                    if square.getAttrib("entry_point"):
                        self.feedback("Spawn", PionGame.INFO)
                        self.sub_state = PionGame.P2_SELECT_SPAWN_PIECE
                    else:
                        self.feedback("Invalid attacker", PionGame.ERR)
                else:
                    self.board.removePiece(square)
                    self.selected_piece = square
                    self.original_loc = (x, y)
                    self.feedback("Move {}".format(square.getAttrib("name")), PionGame.INFO)
                    self.sub_state = PionGame.P2_MOVE_ATTACKING_PIECE
            elif self.sub_state == PionGame.P2_SELECT_DEFENDING_PIECE:
                if not defender:
                    self.feedback("Invalid defender", PionGame.ERR)
                else:
                    self.board.removePiece(square)
                    self.selected_piece = square
                    self.original_loc = (x, y)
                    self.feedback("Move {}".format(square.getAttrib("name")), PionGame.INFO)
                    self.sub_state = PionGame.P2_MOVE_DEFENDING_PIECE

    def phase2_place(self, x, y):
        loc = (x, y)
        square = self.board.get(loc)

        if square != Board._Empty:
            Log.info("GOT: [" + str(square) + "]")
            return self.phase2_attack(x, y, square)

        old_state = self.sub_state
        if self.sub_state == PionGame.P2_MOVE_ATTACKING_PIECE:
            next_state = PionGame.P2_SELECT_DEFENDING_PIECE
        else:
            next_state = PionGame.P2_SELECT_ATTACKING_PIECE

        old_loc = self.selected_piece.getLocation()
        Log.info("Game: Move piece {} from {} to {}".format(self.selected_piece.getAttrib("name"), old_loc, loc))
        self.selected_piece.location = old_loc
        try:
            self.board.movePiece(self.selected_piece, loc)
            # If the piece had spawned on top of a spawner then restore the spawner when it moves.
            spawner = self.selected_piece.getAttrib("spawner")
            if spawner != None:
                Log.info("Game: Replace {} at {}.".format(spawner.getAttrib("name"), old_loc))
                self.board.addPiece(spawner)
                self.selected_piece.setAttrib("spawner", None)
            self.selected_piece = None
            self.sub_state = next_state
        except BoardError as bex:
            self.feedback("Invalid square", PionGame.ERR)
            self.sub_state = old_state
            Log.info(bex)

    def phase2_attack(self, x, y, defender):
        attacker = self.selected_piece
        aName = attacker.getAttrib("name")
        dName = defender.getAttrib("name")
        aVal = attacker.getAttrib("attack")
        dVal = defender.getAttrib("defence")
        Log.info("Attack {} ({}) -X- {} ({})".format(aName, aVal, dName, dVal))
        territory = (x,y)

        attacker.setAttrib("revealed", True)
        defender.setAttrib("revealed", True)

        if aVal >= dVal:
            Log.info("  Attack successful")
            attacker.location = territory
            self.board.removePieceAt(territory)
            self.board.addPiece(attacker)
            self.feedback("{} destroyed.".format(dName), PionGame.INFO)
        else:
            Log.info("  Attack failed")
            defender.location = territory
            self.board.removePieceAt(attacker.location)
            self.feedback("{} failed.".format(aName), PionGame.INFO)
            
        if self.sub_state == PionGame.P2_MOVE_ATTACKING_PIECE:
            self.sub_state = PionGame.P2_SELECT_DEFENDING_PIECE
        else:
            self.sub_state = PionGame.P2_SELECT_ATTACKING_PIECE

    def phase2_choose(self, x, y):
        pass

    def skip(self):
        if self.main_state == PionGame.GAME_STATE_PHASE_1:
            self.main_state = PionGame.GAME_STATE_PHASE_2
            self.sub_state = PionGame.P2_SELECT_ATTACKING_PIECE
            #self.board.save("latest.json")
            self.hidePieces()
        elif self.main_state == PionGame.GAME_STATE_PHASE_2: 
            if self.sub_state == PionGame.P2_SELECT_DEFENDING_PIECE:
                self.sub_state = PionGame.P2_SELECT_ATTACKING_PIECE

    def hidePieces(self):
        board = self.board

        for row in range(board.width):
            for col in range(board.height):
                loc = (row,col)
                piece = board.grid[loc]

                if piece != Board._Empty:
                    if not piece.getAttrib("entry_point"):
                        piece.setAttrib("revealed", False)
                    else:
                        piece.setAttrib("revealed", True)



    def getSubStateStr(self):
        if self.main_state == PionGame.GAME_STATE_PHASE_1:
            return PionGame.P1_State_str[self.sub_state]
        else:
            if self.sub_state == PionGame.P2_MOVE_ATTACKING_PIECE or self.sub_state == PionGame.P2_MOVE_DEFENDING_PIECE:
                return PionGame.P2_State_str[self.sub_state].format(self.selected_piece.getAttrib("name"))
            else:
                return PionGame.P2_State_str[self.sub_state]

    def feedback(self, message, level):
        Log.info("[L:{}] {}".format(level, message))
        if self.message.lvl < level:
            self.message = PionGame.FeedbackMsg(message, level)

    def consumeFeedback(self):
        msg = self.message.msg
        lvl = self.message.lvl
        self.message = PionGame.NO_MSG
        return msg, lvl

    def getRound(self):
        if self.main_state == PionGame.GAME_STATE_PHASE_1:
            return PionGame.DEFENCE_ROUND
        else:
            if self.sub_state == PionGame.P2_MOVE_DEFENDING_PIECE or self.sub_state == PionGame.P2_SELECT_DEFENDING_PIECE:
                return PionGame.DEFENCE_ROUND
            else:
                return PionGame.ATTACK_ROUND
