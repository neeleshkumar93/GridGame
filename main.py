# The main file which should be run in order to launch the game.
from pygame.locals import *
from enum import Enum
import pygame
import math

class Scene(Enum):
	create_party = 1
	game_grid = 2

# Game Initialization
screen = pygame.display.set_mode((800,600), DOUBLEBUF)
clock = pygame.time.Clock()
fps = 60
current_scene = Scene.create_party

# Import resources
img_char[0] = pygame.image.load("img/char_0.png")
img_char[1] = pygame.image.load("img/char_1.png")
img_char[2] = pygame.image.load("img/char_2.png")


# Game Loop
while 1:
	dt = clock.tick(fps)
	
	if current_scene == Scene.create_party:
		#...
	elif current_scene == Scene.game_grid:
		#...