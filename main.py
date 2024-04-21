from enemy import Enemy
from player import Player
import pygame
from sys import exit
import math
from settings import *

pygame.init()

# Creating the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top Down Shooter")
clock = pygame.time.Clock()

# Loads images
background = pygame.transform.scale(pygame.image.load("assets/background.png").convert(), (WIDTH, HEIGHT))



all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

for i in range(5):
    enemy = Enemy(screen, all_sprites_group, enemy_group)
    enemy_group.add(enemy)
    all_sprites_group.add(enemy)
    

player = Player(screen, all_sprites_group, bullet_group, enemy_group)
all_sprites_group.add(player)

while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))

    all_sprites_group.draw(screen)
    all_sprites_group.update()
    # pygame.draw.rect(screen, "red", player.hitbox_rect, width=2)
    # pygame.draw.rect(screen, "yellow", player.rect, width=2)

    pygame.display.update()
    clock.tick(FPS)