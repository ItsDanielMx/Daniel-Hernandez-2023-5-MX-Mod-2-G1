import random
import pygame
from pygame import mixer
from pygame.sprite import Sprite
from game.utils.constants import SCREEN_WIDTH, LIFE, LIFE_SOUND, STAR, STAR_SOUND, MISILES, SLOW, SLOW_SOUND, FAST, FAST_SOUND
from game.components.spaceship import Spaceship
from game.components.enemy import Enemy


class Powers(Sprite):
    def __init__(self):
        super().__init__()
        self.image_width = 30
        self.image_height = 30
        self.rect = pygame.Rect(0, 0, self.image_width, self.image_height)
        self.powers_data = [
            {
                'image': LIFE, 
                'rect': self.rect, 
                'type': 'life' 
            },
            {
                'image': STAR,
                'rect': self.rect,
                'type':'invencible'
            },
            {
                'image': MISILES,
                'rect': self.rect,
                'type':'ammo'
            },
            {
                'image': SLOW,
                'rect': self.rect,
                'type':'slow'
            },
            {
                'image': FAST,
                'rect': self.rect,
                'type':'fast'
            }
        ]
        self.powers = []
        self.game_speed = 7
        self.last_power_score = 0
        self.channel6 = mixer.Channel(5)
        self.channel7 = mixer.Channel(6)
        self.bullets = pygame.sprite.Group()
        self.spaceship = Spaceship()
        self.enemy = Enemy()
        self.invencible_time = 0
        


    def create_power(self, score):
        if score % 500 == 0 and score > self.last_power_score:
            x_pos = random.randint(0, SCREEN_WIDTH - self.image_width)
            selected_power = random.choice(self.powers_data)
            power_image = pygame.transform.scale(selected_power['image'], (self.image_width, self.image_height))
            power_rect = selected_power['rect'].copy()
            power_rect.topleft = (x_pos, -self.image_height)
            power = {
                'image': power_image,
                'rect': power_rect,
                'type': selected_power['type']
            }
            self.powers.append(power)
            self.last_power_score = score

    
    def reset(self):
        self.powers.clear()
        self.last_power_score = 0
        self.power_x = 10

    
    def slow_motion(self, enemy, power):
        enemy.game_speed = 1
        self.powers.remove(power)
        pygame.mixer.init()
        pygame.mixer.music.load(SLOW_SOUND)
        self.channel6.set_volume(1)
        self.channel6.play(mixer.Sound(SLOW_SOUND))
        pygame.time.set_timer(enemy.slow_timer, 12000)


    def velocity(self, spaceship, power):
        spaceship.game_speed = 18
        self.powers.remove(power)
        pygame.mixer.init()
        pygame.mixer.music.load(FAST_SOUND)
        self.channel6.set_volume(0.2)
        self.channel6.play(mixer.Sound(FAST_SOUND))
        pygame.time.set_timer(spaceship.velocity_timer, 12000)


    def invencible(self, spaceship, power):
        spaceship.is_invencible = True
        self.powers.remove(power)
        pygame.mixer.init()
        pygame.mixer.music.load(STAR_SOUND)
        self.channel7.set_volume(2)
        self.channel7.play(mixer.Sound(STAR_SOUND))
        pygame.time.set_timer(spaceship.shield_timer, 12000)


    def extra_life(self, spaceship, power):
        spaceship.lifes += 1
        self.powers.remove(power)
        pygame.mixer.init()
        pygame.mixer.music.load(LIFE_SOUND)
        self.channel6.set_volume(0.4)
        self.channel6.play(mixer.Sound(LIFE_SOUND))


    def doble_ammo(self, spaceship, power):
        spaceship.is_doble_ammo = True
        self.powers.remove(power)
        pygame.time.set_timer(spaceship.doble_ammo_timer, 12000)


    def check_spaceship_colli(self, spaceship, enemies):
        for power in self.powers:
            if power['rect'].colliderect(spaceship.rect) and spaceship.is_alive:
                if power['type'] == 'life':
                    self.extra_life(spaceship, power)
                elif power['type'] == 'invencible':
                    self.invencible(spaceship, power)
                elif power['type'] == 'ammo':
                    self.doble_ammo(spaceship, power)
                elif power['type'] == 'slow':
                    self.slow_motion(enemies, power)
                elif power['type'] == 'fast':
                    self.velocity(spaceship, power)
                return True
        return False

    def update(self, score):
        self.create_power(score)
        for power in self.powers:
            power['rect'].y += self.game_speed
        if self.invencible_time <= 0:
            pygame.mixer.music.stop()

    def draw(self, screen):
        for power in self.powers:
            screen.blit(power['image'], power['rect'])
