import pygame
from pygame.sprite import Sprite
from game.utils.constants import BULLET, EXPLOSION

class Bullet(Sprite):
    def __init__(self, spaceship_rect, enemies):
        super().__init__()
        self.image_width = 7
        self.image_height = 15
        self.image = BULLET
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = spaceship_rect.centerx
        self.rect.bottom = spaceship_rect.top
        self.speed = 20
        self.enemies = enemies

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

    def check_collision(self, enemies, explosions, explosion):
        for enemy in enemies:
            if self.rect.colliderect(enemy['rect']):
                enemies.remove(enemy)
                self.kill()
                explosion = {
                    'image': explosion,
                    'rect': enemy['rect'].copy(),
                    'start_time': pygame.time.get_ticks()
                }
                explosions.append(explosion)
                return 100  
        return 0  