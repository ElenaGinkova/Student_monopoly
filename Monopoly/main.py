import sys
import pygame
from .Players import Player
from .Game import Game


game = Game()
game.play()
'''Quit Pygame'''
pygame.quit()
sys.exit()