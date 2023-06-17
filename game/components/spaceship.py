import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH

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

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move_left(self):
        self.rect.x -= self.game_speed
        if self.rect.left < 0:
            self.rect.left = 0

    def move_right(self):
        self.rect.x += self.game_speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def update(self, keyboard_events):
        if keyboard_events[pygame.K_LEFT]:
            self.move_left()
        if keyboard_events[pygame.K_RIGHT]:
            self.move_right()