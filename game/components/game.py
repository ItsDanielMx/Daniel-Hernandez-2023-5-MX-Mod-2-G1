import pygame
from pygame import mixer
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, FONT_SIZE, GAME_OVER, BLINK_DURATION, MARIO_WIN
from game.components.spaceship import Spaceship
from game.components.enemy import Enemy
from game.components.powers import Powers

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
        self.powers = Powers()
        self.score = 0
        self.bullets = pygame.sprite.Group()
        self.font = pygame.font.Font(FONT_STYLE, FONT_SIZE)
        self.game_over = False
        self.score_width = (SCREEN_WIDTH // 2) - 90
        self.score_height = (SCREEN_HEIGHT // 2) + 200
        self.restart_width = (SCREEN_WIDTH // 2) - 160
        self.restart_height = (SCREEN_HEIGHT // 2) + 100
        self.scores = []
        self.high_score = 0
        self.channel2 = mixer.Channel(1)
        self.paused = False


    def run(self):
        self.playing = True
        while self.playing:
            self.handle_events()
            if not self.paused:
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
                if event.key == pygame.K_r:
                    self.restart()
                elif event.key == pygame.K_p:
                    self.toggle_pause()
            if event.type == pygame.USEREVENT + 1:
                self.spaceship.is_invencible = False
            if event.type == pygame.USEREVENT + 2:
                self.spaceship.is_doble_ammo = False
            if event.type == pygame.USEREVENT + 3:
                self.spaceship.game_speed = 12
            if event.type == pygame.USEREVENT + 4:
                self.enemy.game_speed = 7


    def toggle_pause(self):
        self.paused = not self.paused


    def restart(self):
        self.enemy.reset()
        self.powers.reset()
        self.spaceship.reset()
        self.game_over = False
        self.score = 0


    def high_scores(self):
        self.scores.append(self.score)
        self.high_score = max(self.scores)
        if self.game_over:
                if self.high_score > 0 and self.high_score == self.score:
                    pygame.mixer.init()
                    pygame.mixer.music.load(MARIO_WIN)
                    self.channel2.play(mixer.Sound(MARIO_WIN))
    

    def update(self):
        events = pygame.key.get_pressed()
        self.spaceship.update(events)
        self.enemy.update()
        self.spaceship.bullets.update()
        self.powers.check_spaceship_colli(self.spaceship, self.enemy)
        for bullet in self.spaceship.bullets:
            self.score += bullet.check_enemy_collision(self.enemy.enemies, self.enemy.explosions) 
        self.powers.update(self.score)
        for bullet in self.enemy.bullets:
            if bullet.check_spaceship_collision(self.spaceship, self.spaceship.explosions) and self.spaceship.is_invencible == False:
                self.spaceship.lifes -= 1  
                if self.spaceship.lifes == 0:  
                    self.spaceship.is_alive = False
                    self.game_over = True
                    self.high_scores()
                    break
        if self.spaceship.check_ships_collision(self.enemy.enemies, self.spaceship.explosions):
            if self.spaceship.is_invencible:
                self.score += 100
            elif not self.spaceship.is_invencible:
                self.spaceship.lifes -= 1
                if self.spaceship.lifes == 0:
                    self.spaceship.is_alive = False
                    self.game_over = True
                    self.high_scores()
        

    def draw(self):
        self.clock.tick(FPS) 
        self.screen.fill((255, 255, 255)) 
        self.draw_background()
        self.draw_score_pause()
        self.powers.draw(self.screen)
        self.spaceship.draw(self.screen)
        self.enemy.draw(self.screen)
        self.draw_game_over()
        self.draw_pause()
        pygame.display.update() 
        pygame.display.flip()  


    def draw_score_pause(self):
        if self.spaceship.is_alive:
            score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))


    def draw_pause(self):
        current_time = pygame.time.get_ticks()
        visible = (current_time // BLINK_DURATION) % 2 == 0
        if self.paused and visible:
            pause_text = self.font.render("PAUSED", True, (255, 255, 255))
            self.screen.blit(pause_text, ((SCREEN_WIDTH // 2) - 50, SCREEN_HEIGHT // 2))


    def draw_game_over(self):
        if self.game_over:
            current_time = pygame.time.get_ticks()
            visible = (current_time // BLINK_DURATION) % 2 == 0
            game_over_image = pygame.transform.scale(GAME_OVER, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(game_over_image, (0, 0))
            if visible:
                restart_text = self.font.render("PRESS ""R"" TO RESTART", True, (255, 255, 255))
                self.screen.blit(restart_text, (self.restart_width, self.restart_height))
                if self.high_score > 0 and self.high_score == self.score:
                    new_high_score_text = self.font.render("NEW HIGH SCORE!", True, (255, 0, 0))
                    self.screen.blit(new_high_score_text, (self.restart_width + 40, self.restart_height - 250))
            score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (self.score_width, self.score_height))
            high_score_text = self.font.render(f"HIGH SCORE: {self.high_score}", True, (255, 0, 0))
            self.screen.blit(high_score_text, (self.score_width - 78, self.score_height - 50))


    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg)) 
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed