import random
import pygame
from pygame import mixer
from pygame.sprite import Sprite
from game.utils.constants import SCREEN_WIDTH, LIFE, LIFE_SOUND
from game.components.spaceship import Spaceship
from game.components.enemy import Enemy


class Powers(Sprite):
    def __init__(self):
        super().__init__()
        self.image_width = 20
        self.image_height = 20
        self.rect = pygame.Rect(0, 0, self.image_width, self.image_height)
        self.powers_data = [
            {
                'image': LIFE, 
                'rect': self.rect, 
                'type': 'life' 
            }
        ]
        self.powers = []
        self.game_speed = 7
        self.last_power_score = 0
        self.channel6 = mixer.Channel(5)
        self.bullets = pygame.sprite.Group()
        self.spaceship = Spaceship()
        self.enemy = Enemy()


    def create_power(self, score):
        if score % 50 == 0 and score > self.last_power_score:
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


    def check_spaceship_colli(self, spaceship):
        for power in self.powers:
            if power['rect'].colliderect(spaceship.rect) and spaceship.is_alive:
                if power['type'] == 'life':
                    spaceship.lifes += 1
                self.powers.remove(power)
                pygame.mixer.init()
                pygame.mixer.music.load(LIFE_SOUND)
                self.channel6.set_volume(0.1)
                self.channel6.play(mixer.Sound(LIFE_SOUND))
                return True
        return False

    def update(self, score):
        self.create_power(score)
        for power in self.powers:
            power['rect'].y += self.game_speed

    def draw(self, screen):
        for power in self.powers:
            screen.blit(power['image'], power['rect'])
