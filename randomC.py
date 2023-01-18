# randomC.py : 실물 시뮬레이션 할 때 커뮤니티를 드러내는 파일. 사용하지 않는 파일이다.
import pygame as pg
from pygame.locals import *
import sys, random
from obj import *
from draw import Mblit

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((800, 800))

card = Card(random.choice(('Red', 'Blue', 'Yellow', 'Green')), random.randint(1, 7))
f = pg.font.SysFont('Arialrounded', 48)

while True:
    screen.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            card = Card(random.choice(('Red', 'Blue', 'Yellow', 'Green')), random.randint(1, 7))
    
    Mblit(screen, card.img, (400, 400))
    if card.color == 'Red':
        t = f.render("Spade", True, Black)
    if card.color == 'Blue':
        t = f.render("Heart", True, Black)
    if card.color == 'Yellow':
        t = f.render("Diamond", True, Black)
    if card.color == 'Green':
        t = f.render("Clover", True, Black)

    Mblit(screen, t, (400, 600))

    clock.tick(60)
    pg.display.flip()