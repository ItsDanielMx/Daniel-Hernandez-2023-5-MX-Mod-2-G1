import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH
from game.components.bullet import Bullet
from game.components.enemy import Enemy


class Spaceship(Sprite):
    def __init__(self):
        super().__init__()
        self.image_width = 40
        self.image_height = 50
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.game_speed = 10
        self.bullets = pygame.sprite.Group()
        self.enemy = Enemy()
        

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.bullets.draw(screen)

    def move_left(self):
        self.rect.x -= self.game_speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.game_speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def move_up(self):
        self.rect.y -= self.game_speed
        if self.rect.top < 0:
            self.rect.top = 0

    def move_down(self):
        self.rect.y += self.game_speed
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update(self, keyboard_events):
        if keyboard_events[pygame.K_LEFT] or keyboard_events[pygame.K_a]:
            self.move_left()
        if keyboard_events[pygame.K_RIGHT] or keyboard_events[pygame.K_d]:
            self.move_right()
        if keyboard_events[pygame.K_UP] or keyboard_events[pygame.K_w]:
            self.move_up()
        if keyboard_events[pygame.K_DOWN] or keyboard_events[pygame.K_s]:
            self.move_down()
        if keyboard_events[pygame.K_SPACE]:
            self.shoot_bullet()

        self.bullets.update()

    def shoot_bullet(self):
        bullet = Bullet(self.rect, self.enemy.enemies)
        self.bullets.add(bullet)