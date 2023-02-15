import pygame as pg
from pygame.locals import *
import sys, time, random
from obj import *
from draw import Mblit, NS

pg.init()
clock = pg.time.Clock()

class Nubjuk():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.h = 60
        self.vy = 0
        self.stand_img = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Nubjuk.png')), (60, 60))
        self.lie_img = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Nubjuk_head.png')), (60, 30))
        self.img = self.stand_img
    def __repr__(self):
        return f'{self.x}, {self.y}, {self.vy}'


class Enemy():
    def __init__(self, x, typ):
        self.x = x
        self.typ = typ
        if typ == 1:
            self.img = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'OLEV.png')), (60, 30))
            self.y_up = 30
            self.y_down = 0
        if typ == 2:
            self.img = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Ggariyong.png')), (60, 120))
            self.y_up = 120
            self.y_down = 0
        if typ == 3:
            self.img = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Ponix.png')), (60, 60))
            self.y_up = random.randint(60, 240)
            self.y_down = self.y_up - 60
    def blit(self, screen, nx):
        screen.blit(self.img, (270 - nx + self.x, 270 - self.y_up))


class Dinosaur_game():
    Max_score = 0
    def __init__(self, hide = True):
        if hide: self.playing = 'HIDE'
        else:    self.playing = 'PLAY'
        self.screen = pg.Surface((1200, 300))
        self.nubjuk = Nubjuk()
        self.state = 'walking'
        self.enemy_list = []
        self.level = 10
    
    def collide(self, enemy):
        f = 0
        if self.nubjuk.x + 60 > enemy.x and self.nubjuk.x < enemy.x + 60: f += 1
        if self.nubjuk.y + self.nubjuk.h > enemy.y_down and self.nubjuk.y < enemy.y_up: f += 1
        return f == 2

    def draw(self, Uscreen):
        self.screen.fill(Grey2)
        pg.draw.rect(self.screen, Green, (0, 270, 1200, 30))
        self.screen.blit(self.nubjuk.img, (270, 270 - self.nubjuk.y - self.nubjuk.h))
        for enemy in self.enemy_list:
            enemy.blit(self.screen, self.nubjuk.x)
            if self.collide(enemy):
                self.playing = 'STOP'

        score_text     = NS[20].render(f'{int(self.nubjuk.x//10)}', True, Black)
        max_score_text = NS[20].render(f'{int(Dinosaur_game.Max_score//10)}', True, Black)
        Mblit(self.screen, score_text,     (1180, 20), 'TR')
        Mblit(self.screen, max_score_text, (1180, 50), 'TR')
        if int(self.nubjuk.x / (500 + 0.01*self.level)) > int((self.nubjuk.x - self.level) / (500 + 0.01*self.level)) and self.playing == 'PLAY' and random.random() < 1/2:
            self.enemy_list.append(Enemy(self.nubjuk.x + 1200, random.randint(1, 3)))
            if len(self.enemy_list) > 10:
                self.enemy_list.remove(self.enemy_list[0])

        if self.playing == 'PLAY':
            self.nubjuk.x += self.level
            self.nubjuk.y += self.nubjuk.vy
            if Dinosaur_game.Max_score < self.nubjuk.x:
                Dinosaur_game.Max_score = self.nubjuk.x
            if self.nubjuk.y < 0:
                self.nubjuk.y = 0
                self.nubjuk.vy = 0
                self.state = 'walking'
            if self.state == 'jumping':
                self.nubjuk.vy -= 1.5
            self.level = 10 + 0.0002 * self.nubjuk.x

        Mblit(Uscreen, self.screen, (800, 400), rel_pos = False)

    def event(self, out_event, key_pressed):
        for event in out_event:
            if event.type == KEYDOWN:
                if self.state == 'walking' and (event.key == K_SPACE or event.key == K_UP):
                    self.state = 'jumping'
                    self.nubjuk.img = self.nubjuk.stand_img
                    self.nubjuk.h = 60
                    self.nubjuk.vy = 22.5
        key = key_pressed
        if key[K_DOWN]:
            if self.state == 'walking':
                self.nubjuk.img = self.nubjuk.lie_img
                self.nubjuk.h = 30
            if self.state == 'jumping':
                self.nubjuk.img = self.nubjuk.stand_img
                self.nubjuk.h = 60
                self.state = 'dropping'
                self.nubjuk.vy = -22.5
        else:
            self.nubjuk.img = self.nubjuk.stand_img
            self.nubjuk.h = 60

if __name__ == '__main__':
    game = Dinosaur_game()
    game.screen = pg.display.set_mode((1200, 300))
    # game.play()
