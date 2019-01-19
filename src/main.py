from app_config import AppConfig
import sys, os

from pionheart.piongame import PionGame
from pionheart.pionboard import PionBoard
from pionheart.pionpiece import PionPiece
from pionheart.pioncursescontroller import PionCursesController
from pionheart.piontextcontroller import PionTextController
from pionheart.pionaicontroller import PionAIController
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
primary_input = config.get("input", "primary")

if primary_input == "curses":
    primary_controller = PionCursesController(game, board)
elif primary_input == "text":
    primary_controller = PionTextController(game, board)

secondary_input = config.get("input", "secondary")

if secondary_input == "ai":
    secondary_controller = PionAIController(game, board)
elif secondary_input == "net":
    secondary_controller = PionNetController(game, board)

rendermode = config.get("graphics", "renderer")
print "1st Input [" + primary_input + "]"
print "2nd Input [" + secondary_input + "]"
print "Render [" + rendermode + "]"

if rendermode == "curses":
    renderer = PionCursesRenderer(game, primary_controller)
elif rendermode == "pihat":
    renderer = PionHatRenderer(game, primary_controller)
elif rendermode == "kivy":
    renderer = PionKivyRenderer(game, primary_controller)

primary_attacker = config.get("game", "primary") == "attacker"

#TODO: Should not assume there is only one controller.
def game_loop():
    global primary_controller, secondary_controller
    while game.running:
        renderer.render()
        if (game.getRound() == PionGame.DEFENCE_ROUND and not primary_attacker) or (PionGame.ATTACK_ROUND and primary_attacker):
            primary_controller.getInput()
        else:
            secondary_controller.getInput()

if rendermode == "curses":
    from curses import wrapper

    def curses_loop(stdscr):
        renderer.init(stdscr)
        if primary_input == "curses":
            primary_controller.hookUp(stdscr)
        game_loop()

    wrapper(curses_loop)
else:
    game_loop()

