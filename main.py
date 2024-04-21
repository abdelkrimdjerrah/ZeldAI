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
team_A = pygame.sprite.Group()
team_B = pygame.sprite.Group()


for i in range(10):
    player_A = Player(screen, all_sprites_group, bullet_group, team_B, 'A')
    player_B = Player(screen, all_sprites_group, bullet_group, team_A, 'B')
    all_sprites_group.add(player_A)
    all_sprites_group.add(player_B)
    team_A.add(player_A)
    team_B.add(player_B)



while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))

    all_sprites_group.draw(screen)
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)