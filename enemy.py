import pygame
import random
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, all_sprites_group, enemy_group):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("assets/0.png").convert_alpha(), 0, PLAYER_SIZE)
        self.rect = self.image.get_rect()
        self.pos = pygame.math.Vector2(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        self.rect.center = self.pos
        self.all_sprites_group = all_sprites_group
        self.enemy_group = enemy_group  # Group to which this enemy belongs
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2(0, 0)

    def move_randomly(self):
        self.rect.center = self.pos
        prev_pos = self.pos.copy()

        # keep a copy of the current position

        # Randomly choose a target direction
        target_direction = pygame.math.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))

        # Apply gradual change in velocity towards the target direction
        acceleration = 0.1  # Adjust acceleration factor to control the speed of direction change
        self.direction += (target_direction - self.direction) * acceleration

        # Normalize the direction vector to maintain constant speed
        if self.direction.length() > 0:
            self.direction.normalize_ip()

        # Move the player in the current direction
        self.pos += self.direction * self.speed

        ## Check collision with borders
        if self.pos.x < 0:
            self.pos.x = 0
            self.direction.x = 1
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
            self.direction.x = -1
        if self.pos.y < 0:
            self.pos.y = 0
            self.direction.y = 1
        if self.pos.y > HEIGHT:
            self.pos.y = HEIGHT
            self.direction.y = -1


    def update(self):
        # Move randomly
        self.move_randomly()
