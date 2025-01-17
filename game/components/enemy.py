import pygame
import random
from pygame import mixer
from pygame.sprite import Sprite
from game.utils.constants import ENEMY_1, ENEMY_2, EXPLOSION, SCREEN_HEIGHT, SCREEN_WIDTH, ENEMY_LASER, BULLET_ENEMY
from game.components.bullet import Bullet


class Enemy(Sprite):
    def __init__(self):
        self.image_width = 40
        self.image_height = 50
        self.enemy_images = [ENEMY_1, ENEMY_2]
        self.explosion = EXPLOSION
        self.explosion = pygame.transform.scale(self.explosion, (self.image_width, self.image_height))
        self.rect = pygame.Rect(0, 0, self.image_width, self.image_height)
        self.game_speed = 7
        self.enemies = []
        self.explosions = []
        self.enemy_creation_timer = pygame.time.get_ticks()
        self.direction_change_timer = pygame.time.get_ticks()
        self.bullets = pygame.sprite.Group()
        self.last_shot_time = 0
        self.channel5 = mixer.Channel(4)
        self.slow_timer = pygame.USEREVENT + 4


    def create_enemy(self):
        current_time = pygame.time.get_ticks()
        time_delay = random.randint(1000, 1500)

        if current_time - self.enemy_creation_timer > time_delay:
            x_pos = random.randint(0, SCREEN_WIDTH - self.image_width)
            selected_image = random.choice(self.enemy_images)
            enemy_image = pygame.transform.scale(selected_image, (self.image_width, self.image_height))
            enemy = {
                'image': enemy_image,
                'rect': self.rect.copy(),
                'move_direction': random.choice(["left", "right"]),
                'last_shot_time': 0
            }
            enemy['rect'].topleft = (x_pos, -self.image_height)
            self.enemies.append(enemy)
            self.enemy_creation_timer = current_time

    
    def shoot_bullet(self, enemy):
        current_time = pygame.time.get_ticks()
        if current_time - enemy['last_shot_time'] > 1000:
            bullet = Bullet(enemy['rect'], [], "down", BULLET_ENEMY)  
            self.bullets.add(bullet)
            pygame.mixer.init()
            pygame.mixer.music.load(ENEMY_LASER)
            self.channel5.set_volume(0.1) 
            self.channel5.play(mixer.Sound(ENEMY_LASER))
            enemy['last_shot_time'] = current_time  

    
    def reset(self):
        self.enemies.clear()
        for bullet in self.bullets:
            bullet.kill()
        self.game_speed = 7


    def update(self):
        self.create_enemy()
        direction_change_delay = random.randint(500, 1000)
        self.bullets.update()
        for enemy in self.enemies:
            enemy['rect'].y += self.game_speed
            self.update_enemy_position(enemy)
            self.shoot_bullet(enemy)
            self.bullets.update()
            if enemy['rect'].top > SCREEN_HEIGHT:
                self.enemies.remove(enemy)
            else:
                current_time = pygame.time.get_ticks()

                if current_time - self.direction_change_timer > direction_change_delay:
                    new_direction = random.choice(["left", "right"])
                    if new_direction != enemy['move_direction']:
                        enemy['move_direction'] = new_direction
                    else:
                        enemy['move_direction'] = "left" if enemy['move_direction'] == "right" else "right"

                    self.direction_change_timer = current_time
        for explosion in self.explosions:
            current_time = pygame.time.get_ticks()
            if current_time - explosion['start_time'] > 500: 
                self.explosions.remove(explosion)

    def update_enemy_position(self, enemy):
        if enemy['move_direction'] == "left":
            enemy['rect'].x -= self.game_speed
            if enemy['rect'].left < 0:
                enemy['move_direction'] = "right"
        elif enemy['move_direction'] == "right":
            enemy['rect'].x += self.game_speed
            if enemy['rect'].right > SCREEN_WIDTH:
                enemy['move_direction'] = "left"


    def draw(self, screen):
        for enemy in self.enemies:
            screen.blit(enemy['image'], enemy['rect'])
        for explosion in self.explosions:
            screen.blit(self.explosion, explosion['rect'])
        self.bullets.draw(screen)