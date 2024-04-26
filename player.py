import random
from bullet import Bullet
import pygame
from sys import exit
import math
from settings import *
import numpy as np

class Player(pygame.sprite.Sprite):
    def __init__(self,screen, all_sprites_group, bullet_group, enemy_group, team):
        super().__init__()
        self.team = team
        self.pos = pygame.math.Vector2(random.randrange(WIDTH), random.randrange(HEIGHT))
        # Load image based on team
        if self.team == 'A':
            self.image = pygame.transform.rotozoom(pygame.image.load("assets/player_A.png").convert_alpha(), 0, PLAYER_SIZE)
              # Team A starts from the left side
            # self.pos = pygame.math.Vector2(random.randrange(WIDTH//2), random.randrange(HEIGHT))
        elif self.team == 'B':
            self.image = pygame.transform.rotozoom(pygame.image.load("assets/player_B.png").convert_alpha(), 0, PLAYER_SIZE)
            # Team B starts from the right side
            # self.pos = pygame.math.Vector2(random.randrange(WIDTH//2, WIDTH), random.randrange(HEIGHT))
        else:
            # Default to player_A.png if team is not recognized
            self.team = 'A'
            self.image = pygame.transform.rotozoom(pygame.image.load("assets/player_A.png").convert_alpha(), 0, PLAYER_SIZE)
        
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.angle = random.uniform(0, 360)
        self.shoot_cooldown = 0
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)
        self.all_sprites_group = all_sprites_group
        self.bullet_group = bullet_group
        self.screen = screen
        self.enemy_group = enemy_group
        self.velocity_x = 0
        self.velocity_y = 0
        self.rotation_speed = 0.01
        self.direction = pygame.math.Vector2(0, 0)
        self.kills = 0
        self.alive = True
        self.target_enemy = None




 

    def is_shooting(self): 
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.enemy_group)
            self.bullet_group.add(self.bullet)
            self.all_sprites_group.add(self.bullet)
            
    def move_towards_target(self):
        if self.target_enemy is not None and self.target_enemy.alive:
            target_direction = self.target_enemy.pos - self.pos
            target_direction.normalize_ip()  
            acceleration = 0.15  
            self.direction += (target_direction - self.direction) * acceleration
            if self.direction.length() > 0:
                self.direction.normalize_ip()
            self.pos += self.direction * self.speed

    def move_randomly(self):
        self.rect.center = self.pos
        prev_pos = self.pos.copy()
        target_direction = pygame.math.Vector2(random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        acceleration = 0.1  
        self.direction += (target_direction - self.direction) * acceleration
        if self.direction.length() > 0:
            self.direction.normalize_ip()
        self.pos += self.direction * self.speed
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

    def move(self):
        prev_pos = self.pos.copy()
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
        self.hitbox_rect.center = self.pos
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
        



    def ray_casting(self):
        ox, oy = self.pos
        cur_angle = math.radians(self.angle - HALF_FOV)  
        enemy_detected = False
        for ray in range(NUM_RAYS):
            sin_a, cos_a = math.sin(cur_angle), math.cos(cur_angle)
            end_pos = (x, y) = (ox + MAX_DEPTH * cos_a, oy + MAX_DEPTH * sin_a)
            # pygame.draw.line(self.screen, (255,255,255) , self.pos, end_pos, 2)

            for enemy in self.enemy_group:
                if not enemy.alive:
                    continue

                direction_to_enemy = pygame.math.Vector2(enemy.pos - self.pos)

                if direction_to_enemy.length() == 0:
                    continue

                direction_to_enemy.normalize_ip()

                angle_to_enemy = math.degrees(math.acos(direction_to_enemy.dot(pygame.math.Vector2(cos_a, sin_a))))

                if angle_to_enemy <= FOV:
                    target_angle = math.degrees(math.atan2(enemy.pos[1] - self.pos[1], enemy.pos[0] - self.pos[0]))
                    angle_difference = target_angle - self.angle
                    self.angle += min(abs(angle_difference), 1) * np.sign(angle_difference)
                    self.angle %= 360 
                    enemy_detected = True
                    break

            if enemy_detected:
                self.target_enemy = enemy
                self.is_shooting()
                break

            cur_angle += DELTA_ANGLE




    def random_rotation(self):
        random_angle = random.uniform(-180, 180)
        self.angle += (random_angle - self.angle) * self.rotation_speed
        self.angle %= 360
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center=self.hitbox_rect.center)

    def update_kills(self):
        bullets = [bullet for bullet in self.bullet_group if bullet.kills > 0]
        self.kills = sum(bullet.kills for bullet in bullets)


    def update(self):

        if not self.alive:

            self.image = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA)
            return
        
        self.move()
        # self.move_randomly()
        self.random_rotation()
        self.ray_casting()
        self.move_towards_target()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        self.update_kills()
        # Print the updated kills value
        # if(self.kills > 0):
            # print(f"Player kills: {self.kills}")
