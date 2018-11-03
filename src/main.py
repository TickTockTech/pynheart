from app_config import AppConfig
import sys, os

from pionheart.piongame import PionGame
from pionheart.pionboard import PionBoard
from pionheart.pionpiece import PionPiece
from pionheart.pioncursescontroller import PionCursesController
from pionheart.piontextcontroller import PionTextController
from pionheart.pioncursesrenderer import PionCursesRenderer
from pionheart.pionkivyrenderer import PionKivyRenderer
from pionheart.pionhatrenderer import PionHatRenderer

from gamelog import Log

config = AppConfig()
width = int( config.get("board", "width", 8) )
height = int( config.get("board", "height", 8) )

def create_board(width, height):
    board = PionBoard(width, height)

    core = PionPiece.getPiece( "CentralCore", (4,4) )
    bomb1 = PionPiece.getPiece( "DisassemblyMine", (2,4) )
    bomb2 = PionPiece.getPiece( "DisassemblyMine", (4, 2) )
    bomb3 = PionPiece.getPiece( "DisassemblyMine", (5, 6) )
    antivirus1 = PionPiece.getPiece( "AntiVirus", (5, 5) )
    antivirus2 = PionPiece.getPiece( "AntiVirus", (3, 3) )
    entry1 = PionPiece.getPiece( "EntryTile", (0, 0) )
    entry2 = PionPiece.getPiece( "EntryTile", (7, 7) )

    board.addPieces([core, bomb1, bomb2, bomb3, antivirus1, antivirus2, entry1, entry2])

    virus = PionPiece.getPiece( "Virus", (0, 3) )
    corekiller = PionPiece.getPiece( "CoreKiller", (0, 2) )
    portprobe = PionPiece.getPiece( "PortProbe", (0, 4) )

    board.addPieces([virus, corekiller, portprobe])

    board.save("game.json")

    print board.toString()

pieces_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "pieces.json"))
PionPiece.loadPieces(pieces_file)
#create_board(width, height)

#Log.debug("Loading board from file: game.json")
#latest_board = os.path.abspath(os.path.join(os.path.dirname(__file__), "latest.json"))
#board = PionBoard.load(latest_board)
board = PionBoard(8, 8)

game = PionGame(board)
#print board.toString()

# Should be two controllers - attacker and defender.
input_ = config.get("input", "primary")

if input_ == "curses":
    controller = PionCursesController(game, board)
elif input_ == "text":
    controller = PionTextController(game, board)

rendermode = config.get("graphics", "renderer")
print "Input [" + input_ + "]"
print "Render [" + rendermode + "]"

if rendermode == "curses":
    renderer = PionCursesRenderer(game, controller)
elif rendermode == "pihat":
    renderer = PionHatRenderer(game, controller)
elif rendermode == "kivy":
    renderer = PionKivyRenderer(game, controller)

#TODO: Should not assume there is only one controller.
def game_loop():
    while game.running:
        renderer.render()
        controller.getInput()

if rendermode == "curses":
    from curses import wrapper

    def curses_loop(stdscr):
        renderer.init(stdscr)
        if input_ == "curses":
            controller.hookUp(stdscr)
        game_loop()

    wrapper(curses_loop)
else:
    game_loop()

