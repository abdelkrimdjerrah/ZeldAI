import pygame 
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
	def __init__(self):

		# get the display surface 
		self.display_surface = pygame.display.get_surface()

		# sprite group setup
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# sprite setup
		self.create_map()

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('./map/map_FloorBlocks.csv'),
			'grass': import_csv_layout('./map/map_Grass.csv'),
			'object': import_csv_layout('./map/map_Objects.csv'),
		}
		graphics = {
			'grass': import_folder('./graphics/Grass'),
			'objects': import_folder('./graphics/objects')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'grass',random_grass_image)

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

		self.all_players_group = pygame.sprite.Group()

		
		# Create players for team A
		self.team_A_players = pygame.sprite.Group()
		for _ in range(15):
			player_A = Player((2000, 1330), [self.visible_sprites], self.obstacle_sprites, self.all_players_group, 'team_A')
			self.team_A_players.add(player_A)

		# Create players for team B
		self.team_B_players = pygame.sprite.Group()
		for _ in range(15):
			player_B = Player((2300, 1530), [self.visible_sprites], self.obstacle_sprites, self.all_players_group, 'team_B')
			self.team_B_players.add(player_B)

	def run(self):
		all_players = self.team_A_players.sprites() + self.team_B_players.sprites()
		self.visible_sprites.custom_draw(all_players)
		self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup 
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('./graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self, players):
		# Getting the offset based on the center of the first player
		if players:
			player_rect = players[0].rect
			self.offset.x = player_rect.centerx - self.half_width
			self.offset.y = player_rect.centery - self.half_height

		# Drawing the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		# Drawing all sprites
		for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)

