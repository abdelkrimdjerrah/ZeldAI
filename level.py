import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from grass import Grass

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = pygame.sprite.Group()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):

		# Now that the player sprite is created, create grass sprites
		for row_index, row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'x':
					Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
				else: 
					Grass((x, y), [self.visible_sprites])

		for row_index, row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				x = col_index * TILESIZE
				y = row_index * TILESIZE
				if col == 'p':
					self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites)

					
					

	def run(self):
		# update and draw the game
		self.visible_sprites.update()
		self.visible_sprites.draw(self.display_surface)
		debug(self.player.direction)
