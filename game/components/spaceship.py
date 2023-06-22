import pygame
from pygame import mixer
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, SCREEN_HEIGHT, SCREEN_WIDTH, EXPLOSION, PAC_MAN_GAME_OVER, LASER, LIFE
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
        self.game_speed = 12
        self.bullets = pygame.sprite.Group()
        self.enemy = Enemy()
        self.last_shot_time = 0
        self.explosion = EXPLOSION
        self.explosion = pygame.transform.scale(self.explosion, (self.image_width, self.image_height))
        self.explosions = []
        self.is_alive = True
        self.channel1 = mixer.Channel(0)
        self.channel4 = mixer.Channel(3)
        self.life = LIFE
        self.life = pygame.transform.scale(self.life, (20, 20))
        self.lifes = 1
        self.power_x = 10


    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.image, self.rect)
            self.bullets.draw(screen)
            for explosion in self.explosions:
                screen.blit(self.explosion, explosion['rect'])
            for _ in range(self.lifes):
                screen.blit(self.life, (self.power_x, 50))
                self.power_x += self.life.get_width() + 10  
            self.power_x = 10
        else:
            for explosion in self.explosions:
                screen.blit(self.explosion, explosion['rect'])


    def move_left(self):
        if self.is_alive:
            self.rect.x -= self.game_speed
            if self.rect.left < 0:
                self.rect.left = 0


    def move_right(self):
        if self.is_alive:
            self.rect.x += self.game_speed
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH


    def move_up(self):
        if self.is_alive:
            self.rect.y -= self.game_speed
            if self.rect.top < 0:
                self.rect.top = 0

    def move_down(self):
        if self.is_alive:
            self.rect.y += self.game_speed
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT


    def shoot_bullet(self):
        if self.is_alive:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > 200:
                bullet = Bullet(self.rect, self.enemy.enemies, "up")
                self.bullets.add(bullet)
                pygame.mixer.init()
                pygame.mixer.music.load(LASER)
                self.channel4.set_volume(0.2) 
                self.channel4.play(mixer.Sound(LASER))
                self.last_shot_time = current_time


    def check_ships_collision(self, enemies, explosions):
        if self.is_alive:
            for enemy in enemies:
                if self.rect.colliderect(enemy['rect']):
                    enemies.remove(enemy)
                    explosions.append({'image': enemy['image'], 'rect': enemy['rect'], 'start_time': pygame.time.get_ticks()})
                    self.explosions.append({'image': self.image, 'rect': self.rect, 'start_time': pygame.time.get_ticks()})
                    pygame.mixer.init()
                    pygame.mixer.music.load(PAC_MAN_GAME_OVER)
                    self.channel1.play(mixer.Sound(PAC_MAN_GAME_OVER))
                    self.lost_life()
                    return True
            return False
    

    def lost_life(self):
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10

    def reset(self):
        self.lifes = 1
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.is_alive = True

    def update(self, keyboard_events):
        if self.is_alive:
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

        for explosion in self.explosions:
            current_time = pygame.time.get_ticks()
            if current_time - explosion['start_time'] > 500:
                self.explosions.remove(explosion)

        self.bullets.update()