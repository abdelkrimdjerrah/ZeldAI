import random
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


for i in range(MAX_TEAM_SIZE):
    genetic_player_A = Player(screen, all_sprites_group, bullet_group, team_B, 'A')
    all_sprites_group.add(genetic_player_A)
    team_A.add(genetic_player_A)

for i in range(MAX_TEAM_SIZE):
    genetic_player_B = Player(screen, all_sprites_group, bullet_group, team_A, 'B')
    all_sprites_group.add(genetic_player_B)
    team_B.add(genetic_player_B)




def check_game_end():
    team_A_alive = any(player.alive for player in team_A) 
    team_B_alive = any(player.alive for player in team_B) 
    return not (team_A_alive and team_B_alive) 

def genetic_selection(players):
    total_score = sum(player.score for player in players)
    for player in players:
        player.probability = player.score / total_score
    
    selected_player = random.choices(players, [player.probability for player in players])[0]
    return selected_player


def restart_game():
    # Respawn all players
    for player in team_A:
        if(player.alive == False):
            # player.kill()
            # new_player = Player(screen, all_sprites_group, bullet_group, team_B, 'A')
            # all_sprites_group.add(new_player)
            # team_A.add(new_player)
            # player = new_player
            player.alive = True
            player.pos = pygame.math.Vector2(random.randrange(WIDTH//2), random.randrange(HEIGHT))
    
    for player in team_B:
        if(player.alive == False):
            # player.kill()
            # new_player = Player(screen, all_sprites_group, bullet_group, team_A, 'B')
            # all_sprites_group.add(new_player)
            # team_B.add(new_player)
            # player = new_player
            player.alive = True
            player.pos = pygame.math.Vector2(random.randrange(WIDTH//2, WIDTH), random.randrange(HEIGHT))

round = 1
while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0, 0))
    
    if check_game_end():

        restart_game()
        print("____________________________")
        print("Game Over")
        print("____________________________")
        winning_team = 'A' if any(player.alive for player in team_A) else 'B'
        print(f"Team {winning_team} won!")
        print("____________________________")
        players_sprites = [sprite for sprite in all_sprites_group.sprites() if isinstance(sprite, Player)]
        mvp = max(players_sprites, key=lambda x: x.kills)
        for player in players_sprites:
            print(f"Player {player.name} of team {player.team} killed {player.kills} players with score of {player.score}")

        print("____________________________")
        print(f"Player {mvp.name} is the MVP with {mvp.kills} kills")
        print("____________________________")
        selected_genetic_player = genetic_selection(players_sprites)
        print(f"Genetic selection: Player {selected_genetic_player.name} of team {selected_genetic_player.team} is selected for genetic algorithm for round {round}")
        print("____________________________")

        for player in players_sprites:
            player.kills = 0

        round += 1


    all_sprites_group.draw(screen)
    all_sprites_group.update()

    pygame.display.update()
    clock.tick(FPS)