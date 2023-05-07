import pygame
import sys
import os.path
from src.game.game import Game
from src.core.loader import Loader

loader = Loader(os.path.join(os.path.dirname(__file__), 'conf'))
conf = loader.load_json('game_conf')

pygame.init()
# pygame.mixer.init()

game = Game(os.path.join(os.path.dirname('__file__'), 'assets'), conf)
game.play()

pygame.quit()
sys.exit()
