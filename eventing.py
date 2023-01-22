import pygame as pg
from pygame.locals import *
from obj import *
pg.init()

def mouse_main(var):
    mode, player1 = var

    pos = pg.mouse.get_pos()
    if in_rect(pos, (600, 600, 400, 100)):
        mode = 'choose_key'
        player1.key = 11
    
    return mode

def key_choose_key(const, var):
    event = const
    player1, tickf1, tickf2 = var

    if event.key == K_UP:
        player1.key += 10
        tickf1 = 30
        if player1.key > 270:
            player1.key -= 260
    if event.key == K_DOWN:
        player1.key -= 10
        tickf1 = 30
        if player1.key < 10:
            player1.key += 260
    if event.key == K_RIGHT:
        player1.key += 1
        tickf2 = 30
        if player1.key%10 == 9:
            player1.key -= 8
    if event.key == K_LEFT:
        player1.key -= 1
        tickf2 = 30
        if player1.key%10 == 0:
            player1.key += 8
    
    return player1, tickf1, tickf2