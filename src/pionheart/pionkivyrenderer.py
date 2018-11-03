import kivy
import sys, os

kivy.require('1.9.0')

from kivy.utils import platform

from boardgame.renderer import Renderer
from boardgame.game import Game
from boardgame.board import Board
from .pionboard import PionBoard
from gamelog import Log

Log.info("KIVY: Platform {}".format(platform))

# More realistic look on windows
if platform == 'win':
    from kivy.config import Config
    Config.set('graphics', 'width', '550')
    Config.set('graphics', 'height', '900')
    Config.set('graphics', 'resizable', 0)
if platform == 'macosx':
    from kivy.config import Config
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '600')
    Config.set('graphics', 'resizable', 0)

from gamelog import Log

class PionKivyRenderer(Renderer):

    def __init__(self, game, controller):
        super(PionKivyRenderer, self).__init__(game)

        self.controller = controller
        self.render_skew = Renderer.ATTACK_SKEW

    def render(self):
    	pass