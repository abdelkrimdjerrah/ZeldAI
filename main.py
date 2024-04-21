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
    genetic_player_A = Player(screen, all_sprites_group, bullet_group, team_B, 'A')
    all_sprites_group.add(genetic_player_A)
    team_A.add(genetic_player_A)

for i in range(10):
    genetic_player_B = Player(screen, all_sprites_group, bullet_group, team_A, 'B')
    all_sprites_group.add(genetic_player_B)
    team_B.add(genetic_player_B)




def check_game_end():
    team_A_alive = any(player.alive for player in team_A) 
    team_B_alive = any(player.alive for player in team_B) 
    return not (team_A_alive and team_B_alive) 

def restart_game():
    all_sprites_group.empty()
    bullet_group.empty()
    team_A.empty()
    team_B.empty()

    for i in range(10):
        genetic_player_A = Player(screen, all_sprites_group, bullet_group, team_B, 'A')
        all_sprites_group.add(genetic_player_A)
        team_A.add(genetic_player_A)

    for i in range(10):
        genetic_player_B = Player(screen, all_sprites_group, bullet_group, team_A, 'B')
        all_sprites_group.add(genetic_player_B)
        team_B.add(genetic_player_B)


round = 1
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    
    # Check if the game has ended and only one round is played
    if check_game_end() and round == 1:

        # restart_game()
        print("Game Over")
        winning_team = 'A' if any(player.alive for player in team_A) else 'B'
        print(f"Team {winning_team} won!")
        round += 1


    all_sprites_group.draw(screen)
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)