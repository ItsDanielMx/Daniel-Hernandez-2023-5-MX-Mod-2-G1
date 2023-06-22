import pygame
from pygame import mixer
from pygame.sprite import Sprite
from game.utils.constants import BULLET_ENEMY, SCREEN_HEIGHT, PAC_MAN_GAME_OVER, EXPLOSION_SOUND

class Bullet(Sprite):
    def __init__(self, shooter_rect, enemies, direction):
        super().__init__()
        self.image_width = 7
        self.image_height = 15
        self.image = BULLET_ENEMY
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = shooter_rect.centerx
        if direction == "up":
            self.rect.bottom = shooter_rect.top
        elif direction == "down":
            self.rect.top = shooter_rect.bottom
        self.speed = 10
        self.enemies = enemies
        self.direction = direction
        self.channel1 = mixer.Channel(0)
        self.channel3 = mixer.Channel(2)


    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.kill()
        elif self.direction == "down":
            self.rect.y += self.speed
            if self.rect.top > SCREEN_HEIGHT:
                self.kill()

    def check_enemy_collision(self, enemies, explosions):
        for enemy in enemies:
            if self.rect.colliderect(enemy['rect']):
                enemies.remove(enemy)
                self.kill()
                explosions.append({'image': enemy['image'], 'rect': enemy['rect'], 'start_time': pygame.time.get_ticks()})
                pygame.mixer.init()
                pygame.mixer.music.load(EXPLOSION_SOUND)
                self.channel3.set_volume(0.2) 
                self.channel3.play(mixer.Sound(EXPLOSION_SOUND))
                return 100 
        return 0 
    
    def check_spaceship_collision(self, spaceship, explosions):
        if self.rect.colliderect(spaceship.rect) and spaceship.is_alive:
            self.kill()
            explosions.append({'image': spaceship.image, 'rect': spaceship.rect, 'start_time': pygame.time.get_ticks()})
            pygame.mixer.init()
            pygame.mixer.music.load(PAC_MAN_GAME_OVER)
            self.channel1.play(mixer.Sound(PAC_MAN_GAME_OVER))
            spaceship.lost_life()
            return True
        return False