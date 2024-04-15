import random
import pygame 
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, all_players_group, obstacle_sprites, team):
        super().__init__(groups)
        self.image = pygame.image.load('./graphics/player_A.png').convert_alpha() 
        if team == 'team_A':
            self.image_path = './graphics/player_A.png'
        elif team == 'team_B':
            self.image_path = './graphics/player_B.png' 
            
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.all_players_group = all_players_group
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()
        self.team = team
        self.speed = 3  
        self.change_direction = 0  
        self.change_direction_max = 60  

        


    def change_target(self):
        self.direction = pygame.math.Vector2(random.choice([-1, 1]), random.choice([-1, 1]))

    def move(self):
        if self.change_direction == self.change_direction_max:
            self.change_target()
            self.change_direction = 0

        # Move horizontally
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')

        # Move vertically
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

        self.change_direction += 1 

    def collision(self, direction):
        for sprite in self.obstacle_sprites:
            if self.rect.colliderect(sprite.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

        # Collisions with other players
        print(self.all_players_group)
        for player in self.all_players_group:
            if player != self and self.rect.colliderect(player.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.rect.right = player.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = player.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.rect.bottom = player.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = player.rect.bottom
                        




    def update(self):
        self.move()