import pygame
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE
from game.components.spaceship import Spaceship
from game.components.enemy import Enemy


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.spaceship = Spaceship()
        self.enemy = Enemy()

    def run(self):
        self.playing = True
        while self.playing:
            self.handle_events()
            self.update()
            self.draw()
        else:
            print("Something ocurred to quit the game!")
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.spaceship.move_left()
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.spaceship.move_right()
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.spaceship.move_down()
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.spaceship.move_up()

    def update(self):
        events = pygame.key.get_pressed() 
        self.spaceship.update(events)
        self.enemy.update()

    def draw(self):
        self.clock.tick(FPS) 
        self.screen.fill((255, 255, 255)) 
        
        self.draw_background()

        self.spaceship.draw(self.screen)

        self.enemy.draw(self.screen)

        pygame.display.update() 
        pygame.display.flip()  

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg)) 
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed