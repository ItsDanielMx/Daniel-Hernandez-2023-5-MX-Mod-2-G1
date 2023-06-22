import pygame
import os
import pygame.mixer
pygame.mixer.init()
# Global Constants
TITLE = "Spaceships Game"
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
FPS = 30
BLINK_DURATION = 500 
IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
FONT_DIR = os.path.join(os.path.dirname(__file__), "..", "utils")
# Assets Constants
ICON = pygame.image.load(os.path.join(IMG_DIR, "Spaceship/spaceship.png"))

SHIELD = pygame.image.load(os.path.join(IMG_DIR, 'Other/shield.png'))

LIFE = pygame.image.load(os.path.join(IMG_DIR, 'Other/life.png'))

STAR = pygame.image.load(os.path.join(IMG_DIR, 'Other/star.png'))

SLOW = pygame.image.load(os.path.join(IMG_DIR, 'Other/slow.png'))

FAST = pygame.image.load(os.path.join(IMG_DIR, 'Other/fast.png'))

MISILES = pygame.image.load(os.path.join(IMG_DIR, 'Other/misiles.png'))

GAME_OVER = pygame.image.load(os.path.join(IMG_DIR, 'Other/GameOver.png'))

MARIO_WIN = os.path.join(IMG_DIR, 'Other', 'mario_win.mp3')

PAC_MAN_GAME_OVER = os.path.join(IMG_DIR, 'Other', 'pacman-dies.mp3')

MISILES_SOUND = os.path.join(IMG_DIR, 'Other', 'missile.mp3')

EXPLOSION_SOUND = os.path.join(IMG_DIR, 'Other', 'explosion.mp3')

LIFE_SOUND = os.path.join(IMG_DIR, 'Other', 'mario-vida.mp3')

STAR_SOUND = os.path.join(IMG_DIR, 'Other', 'mario_star.mp3')

LASER = os.path.join(IMG_DIR, 'Other', 'laser.mp3')

FAST_SOUND = os.path.join(IMG_DIR, 'Other', 'mario-hongo.mp3')

SLOW_SOUND = os.path.join(IMG_DIR, 'Other', 'slow.mp3')

ENEMY_LASER = os.path.join(IMG_DIR, 'Other', 'enemy_laser.mp3')

EXPLOSION = pygame.image.load(os.path.join(IMG_DIR, 'Other/Explosion.png'))

BG = pygame.image.load(os.path.join(IMG_DIR, 'Other/Track.png'))

HEART = pygame.image.load(os.path.join(IMG_DIR, 'Other/SmallHeart.png'))

DEFAULT_TYPE = "default"
SHIELD_TYPE = 'shield'

SPACESHIP = pygame.image.load(os.path.join(IMG_DIR, "Spaceship/spaceship.png"))
SPACESHIP_SHIELD = pygame.image.load(os.path.join(IMG_DIR, "Spaceship/spaceship_shield.png"))
BULLET = pygame.image.load(os.path.join(IMG_DIR, "Bullet/bullet_1.png"))

BULLET_ENEMY = pygame.image.load(os.path.join(IMG_DIR, "Bullet/bullet_2.png"))
ENEMY_1 = pygame.image.load(os.path.join(IMG_DIR, "Enemy/enemy_1.png"))
ENEMY_2 = pygame.image.load(os.path.join(IMG_DIR, "Enemy/enemy_2.png"))

FONT_STYLE = os.path.join(FONT_DIR, "8-bit-hud.ttf")
FONT_SIZE = 30
