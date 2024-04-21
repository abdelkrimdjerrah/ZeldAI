import math

# game settings
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60
TILE = 100
FPS_POS = (WIDTH - 65, 5)

# minimap settings
MAP_SCALE = 1
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

# ray casting settings
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 100
MAX_DEPTH = 1000
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3*DIST * TILE
SCALE = WIDTH // NUM_RAYS

# player settings
player_pos = (HALF_WIDTH+0.00001, HALF_HEIGHT+0.00001)
player_angle = 0
player_speed = 2
ROTATION_SPEED = 0.05
TEAM_A_COLOR = (255, 0, 0)  # Red
TEAM_B_COLOR = (0, 0, 255)  # Blue
#Colors
WHITE        = (255,255,255)
BLACK        = (0,0,0)
CRED         = (228,113,122)
MGREEN       = (76,187,23) 
SBLUE        = (127,199,255)
CADBLUE      = (95,158,160)
SKYBLUE      = (127,199,255)
DARKGREY     = (40,40,40)





# Player settings
PLAYER_START_X = 400
PLAYER_START_Y = 500
PLAYER_SIZE = 0.35
PLAYER_SPEED = 8
GUN_OFFSET_X = 45
GUN_OFFSET_Y = 20

# Bullet settings
SHOOT_COOLDOWN = 10
BULLET_SCALE = 1.4
BULLET_SPEED = 50
BULLET_LIFETIME = 750


TILE_SIZE = 50