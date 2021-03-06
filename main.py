import sys
import pygame
from pygame import *
from settings import *
import random


init()
wind = display.set_mode((wind_width, wind_height))


game = True
score1 = 0
score2 = 0


class GameSprite(sprite.Sprite):
    def __init__(self, x, y, size, image_name):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (size))
        self.rect = Rect([x, y] + size)

    def draw(self):
        wind.blit(self.image, self.rect)


class Player(GameSprite):
    def __init__(self, x, control):
        super().__init__(x, player_y, player_size, 'player.png')
        self.control = control

    def update(self):
        self.draw()
        keys = key.get_pressed()
        if keys[self.control[0]]:
            if self.rect.y >= 5:
                self.rect.y -= player_speed
        if keys[self.control[1]]:
            if self.rect.y <= 395:
                self.rect.y += player_speed


class Ball(GameSprite):
    def __init__(self):
        super().__init__(325, 225, ball_size, 'ball.png')
        self.x_speed = ball_speed * random.choice([1, -1])
        self.y_speed = ball_speed * random.choice([1, -1])

    def update(self, player1: Player, player2: Player):
        global game
        global score1
        global score2
        self.draw()
        if self.rect.y >= 497 or self.rect.y <= 3:
            self.y_speed *= -1
        if self.rect.x <= player1x:
            if not self.rect.colliderect(player1.rect):
                score2 += 1
            self.x_speed *= -1

        if self.rect.x >= 600:
            if not self.rect.colliderect(player2.rect):
                score1 += 1
            self.x_speed *= -1
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed


fps_timer = time.Clock()
player1 = Player(player1x, [K_w, K_s])
player2 = Player(player2x, [K_UP, K_DOWN])
ball = Ball()
main_font = font.SysFont('Arial', 20)
message_area = Rect(message_area_coo)


def game_loop():
    global game
    while game:
        display.update()

        draw.rect(wind, (255, 255, 255), Rect(0, 0, wind_width, wind_height))
        wind.blit(main_font.render(f'Player1: {score1}   Player2: {score2}', False, scoreboard_color), Rect(scoreboard_coo))
        player1.update()
        player2.update()
        ball.update(player1, player2)

        for eve in event.get():
            if eve.type == QUIT:
                game = False

        if score1 >= 10:
            wind.blit(main_font.render('Player 1 win', False, loose_label_color), message_area)
            display.update()
            fps_timer.tick(1 / game_over_time)
            pygame.quit()
            sys.exit()

        if score2 >= 10:
            wind.blit(main_font.render('Player 2 win', False, loose_label_color), message_area)
            display.update()
            fps_timer.tick(1 / game_over_time)
            pygame.quit()
            sys.exit()

        fps_timer.tick(fps)

if __name__ == '__main__':
    game_loop()