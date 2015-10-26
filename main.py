# The main file which should be run in order to launch the game.
from pygame.locals import *
from enum import Enum
import pygame
import math
import ggparty
import ggmap

class Scene(Enum):
	create_party = 1
	game_grid = 2

# Import resources
img_char[0] = pygame.image.load("img/char_0.png")
img_char[1] = pygame.image.load("img/char_1.png")
img_char[2] = pygame.image.load("img/char_2.png")

# Game Initialization
screen = pygame.display.set_mode((800,600), DOUBLEBUF)
clock = pygame.time.Clock()
fps = 60

def switchToScene(Scene sc):
	current_scene = sc
	if sc == Scene.create_party:
		partyCanvas = PartyGrid()
	elif sc == Scene.game_grid:
		mapCanvas = MapGrid()

switchToScene(Scene.create_party)

# Game Loop
while 1:
	dt = clock.tick(fps)
	
	if current_scene == Scene.create_party:
		partyCanvas.renderGrid(screen)
	elif current_scene == Scene.game_grid:
		mapCanvas.renderGrid(screen)