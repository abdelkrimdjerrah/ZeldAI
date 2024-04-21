from bullet import Bullet
import pygame
from sys import exit
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,screen, all_sprites_group, bullet_group, enemy_group):
        super().__init__()
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.image = pygame.transform.rotozoom(pygame.image.load("assets/0.png").convert_alpha(), 0, PLAYER_SIZE)
        self.base_player_image = self.image
        self.hitbox_rect = self.base_player_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.angle = 0
        self.shoot_cooldown = 0
        self.gun_barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y)
        self.all_sprites_group = all_sprites_group
        self.bullet_group = bullet_group
        self.screen = screen
        self.enemy_group = enemy_group
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction = pygame.math.Vector2(0, 0)


    def player_rotation(self):
        self.mouse_coords = pygame.mouse.get_pos()
        self.x_change_mouse_player = (self.mouse_coords[0] - self.hitbox_rect.centerx)
        self.y_change_mouse_player = (self.mouse_coords[1] - self.hitbox_rect.centery)
        self.angle = math.degrees(math.atan2(self.y_change_mouse_player, self.x_change_mouse_player))
        self.image = pygame.transform.rotate(self.base_player_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
       

    def user_input(self):
        self.velocity_x = 0
        self.velocity_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.velocity_y = -self.speed
        if keys[pygame.K_s]:
            self.velocity_y = self.speed
        if keys[pygame.K_d]:
            self.velocity_x = self.speed
        if keys[pygame.K_a]:
            self.velocity_x = -self.speed

        if self.velocity_x != 0 and self.velocity_y != 0: # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]:
            self.shoot = True
            self.is_shooting()
        else:
            self.shoot = False

    def is_shooting(self): 
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = SHOOT_COOLDOWN
            spawn_bullet_pos = self.pos + self.gun_barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_pos[0], spawn_bullet_pos[1], self.angle, self.enemy_group)
            self.bullet_group.add(self.bullet)
            self.all_sprites_group.add(self.bullet)
            

    def move(self):
        # Store previous position for collision resolution
        prev_pos = self.pos.copy()

        # Move player
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

        # Update hitbox position
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
        

        # # Update rect position based on the hitbox position
        # self.rect.center = self.hitbox_rect.center



    def ray_casting(self):
        ox, oy = self.pos
        cur_angle = math.radians(self.angle - HALF_FOV) # Convert player angle to radians
        enemy_detected = False
        for ray in range(NUM_RAYS):
            sin_a, cos_a = math.sin(cur_angle), math.cos(cur_angle)
            end_pos = (x, y) = (ox + MAX_DEPTH * cos_a, oy + MAX_DEPTH * sin_a)
            pygame.draw.line(self.screen, DARKGREY, self.pos, end_pos, 2)
            
            # Check for collision with enemies within FOV
            for enemy in self.enemy_group:
                # Calculate the direction vector from the player to the enemy
                direction_to_enemy = pygame.math.Vector2(enemy.pos - self.pos).normalize()
                
                # Calculate the angle between the player's direction and the direction to the enemy
                angle_to_enemy = math.degrees(math.acos(direction_to_enemy.dot(pygame.math.Vector2(cos_a, sin_a))))
                
                # Check if the enemy is within the player's FOV
                if angle_to_enemy <= HALF_FOV:
                    # If the enemy is within the FOV, point the player towards the enemy
                    self.angle = math.degrees(math.atan2(enemy.pos[1] - self.pos[1], enemy.pos[0] - self.pos[0]))
                    enemy_detected = True
                    break # Exit the loop after detecting one enemy
            
            if enemy_detected:
                break  # Exit the loop if an enemy is detected
            cur_angle += DELTA_ANGLE



            

    def update(self):
        self.user_input()
        self.move()
        self.player_rotation()
        self.ray_casting()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
