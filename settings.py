import math

# game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 5)
MAX_TEAM_PLAYERS = 10

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 100
MAX_DEPTH = 1000
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3*DIST * TILE
SCALE = WIDTH // NUM_RAYS



# Player settings
PLAYER_START_X = 400
PLAYER_START_Y = 500
PLAYER_SIZE = 0.35
PLAYER_SPEED = 1
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20


# Bullet settings
SHOOT_COOLDOWN = 10
BULLET_SCALE = 1.4
BULLET_SPEED = 6
BULLET_LIFETIME = 750

MAX_TEAM_SIZE = 10


TILE_SIZE = 50


# Score
KILL_REWARD = 100
DEATH_PENALTY = 50