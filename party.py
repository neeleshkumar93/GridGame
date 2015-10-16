from enum import Enum
import pygame
import math

class Character(Enum):
	single_shot = 0 	# 1x1 character that can shoot in a single direction
	double_shot = 1     # 1x2 character that can shoot in two directions
	shield = 2          # 2x2 character that cannot shoot at all


# Representation of a single character within a party.
class CharacterSprite(pygame.sprite.Sprite):
	# position: 	(x,y) tuple
	#    angle: 	angle in radians
	# chartype:     value from the Character enum
	def __init__(self, position, angle, chartype):
		self.src_image = pygame.image.load("img/char_"+chartype.value+".png")
		self.rect.topleft = position
		self.rotate(angle)
		self.ghost = 0

	def rotate(self, angle):
		self.rotation = angle
		self.image = pygame.transform.rotate(self.src_image, angle)

	#Increment the current rotation by some amount
	def rotateRelative(self, angle):
		newdegrees = (degrees(self.rotation)+degrees(angle)) % 360
		self.rotate(radians(newdegrees))


# Data Structure for 3x3 Character Parties
class PartyGrid():
	GRID_SIZE = 3
	CELL_SIZE = 32 		  # In pixels
	grid_position = (0,0)
	party_members = []    # Contains CharacterSprite elements. Must be in parallel with array below.
	party_positions = []  # Contains (gridx, gridy) elements. Must be in parallel with array above.
	grid_contents = [[(-1,0,0) for x in range(GRID_SIZE)] for x in range(GRID_SIZE)] # Contains Character enum elements & grid pos of source character.

	def __init__(self):
		# ...

	# Returns 1 if the character was successfully inserted, 0 otherwise.
	# Angles should be in radians, should be between 0 and 2pi, and should always be multiples of pi/2.
	def appendCharacter(self, chartype, angle, gridx, gridy):
		if self.__canPlaceHere(self.__determineOccupyingCells(chartype, angle, gridx, gridy)) == 0:
			return 0
		party_members.append(CharacterSprite((0,0), angle, chartype))
		party_positions.append((gridx, gridy))
		self.__updateGrid()
		return 1

	# Creates a "ghost" image of a character at this location, for previewing purposes.
	# Only one such "ghost" character can be on the grid at any time.
	def previewCharacter(self, chartype, angle, gridx, gridy):
		if self.__canPlaceHere(self.__determineOccupyingCells(chartype, angle, gridx, gridy)) == 0:
			return 0
		self.clearGhosts()
		newchar = CharacterSprite((0,0), angle, chartype)
		newchar.ghost = 1
		party_members.append(newchar)
		party_positions.append((gridx, gridy))
		self.__updateGrid()
		return 1

	#Gets the grid cells (with top-left at (gridx,gridy)) this given character would occupy at the given angle
	def __determineOccupyingCells(self, chartype, angle, gridx, gridy):
		if (chartype == Character.shield):
			return [(gridx,gridy),(gridx+1,gridy),(gridx,gridy+1),(gridx+1,gridy+1)]
		if (chartype == Character.double_shot):
			if angle == 0 or angle == pi or angle == 2*pi:
				return[(gridx,gridy),(gridx+1,gridy)]
			else:
				return[(gridx,gridy),(gridx,gridy+1)]
		return [(gridx,gridy)]

	# Given an array of (gridx, gridy) tuples, returns if it would be valid for a character to be placed there.
	# Returns 1 if it is a valid placement, 0 otherwise.
	def __canPlaceHere(self, gridlist):
		for coord in gridList:
			if self.getCharacter(coord[0],coord[1]) != -1:
				return 0
			for axis in coord:
				if axis < 0 or axis >= self.GRID_SIZE:
					return -1
		return 1

	# Remove all "ghost" characters from the grid
	def clearGhosts(self):
		updatedCharList = []
		updatedPosList = []
		for i in range(len(party_members)):
			if character.ghost != 1:
				updatedList.append(party_members[i])
				updatedPosList.append(party_positions[i])
		party_members = updatedList
		party_positions = updatedPosList

	# Returns 1 if the character was successfully removed, 0, otherwise.
	def removeCharacter(self, gridx, gridy):

	# Returns the number of characters currently placed into this grid.
	def numberOfCharcters(self):
		count = 0
		for member in party_members:
			if member.ghost == 0:
				count += 1
		return count

	# Returns the Character enum of the character occupying this cell of the grid,
	# or -1 if no character is in this cell.
	def getCharacter(self, gridx, gridy):
		if gridx < 0 or gridy < 0 or gridx >= GRID_SIZE or gridy >= GRID_SIZE:
			return -1
		return self.grid_contents[gridx][gridy][0]

	# Rotates the character at (gridx, gridy) counter-clockwise.
	# Returns 1 if the rotation was successful, 0 otherwise.
	def rotateCharacterAt(self, gridx, gridy):
		if self.getCharacter(gridx, gridy) == -1:
			return 0
		findPosition = (self.grid_contents[gridx][gridy][1], self.grid_contents[gridx][gridy][2])
		for i in range(len(party_positions)):
			if party_positions[i] == findPosition:
				party_members[i].rotateRelative(pi/2)
				self.__updateGrid()
				return 1
		return 0

	# Set the position on the screen where the grid should be drawn at
	def gridPosition(self, x, y):
		self.grid_position = (x,y)
		self.__updateGrid()

	# Syncs the contents of the grid_contents array based on the contents of the party_members/party_positions array.
	# Also updates the contents of party_members array based on the contents of the grid_position tuple.
	def __updateGrid(self):

	# Given a pixel coordinate within the game screen, return the cooresponding coordinate within the grid space
	# Returns (-1,-1) if outside the bounds of the grid
	def screenToGridCoords(self, sx, sy):
		if sx < grid_position[0] or sy < grid_position[1] or sx >= grid_position[0]+CELL_SIZE*GRID_SIZE or sy >= grid_position[1]+CELL_SIZE*GRID_SIZE:
			return (-1,-1)
		bx = sx - grid_position[0]
		by = sy - grid_position[1]
		return (math.floor(bx/CELL_SIZE), math.floor(by/CELL_SIZE))

	# Renders the grid on screen
	def renderGrid(self, screen):
		party_members.draw(screen)