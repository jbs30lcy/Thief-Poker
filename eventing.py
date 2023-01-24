import pygame as pg
from pygame.locals import *
from obj import *
pg.init()

def mouse_main(var):
    mode, player1 = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)
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

def mouse_choose_key(var):
    mode = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)
    if in_rect(pos, (1350-45, 750-30, 90, 60)):
        mode = 'chooseRank'

    return mode

def mouse_play(var):
    player1, player2, mode, choose, tick, tickf1 = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)
    
    c1 = len(player1.card_list)
    for i in range(len(player1.card_list)):
        if player1.card_list[i] in player1.showc:
            continue
        x, y = 850 - c1*50 + 100*i, 700
        if i == len(player1.card_list)-1: card_wid = 300
        else: card_wid = 100
        if in_rect(pos, (x - 150, y - 225, card_wid, 600)):
            card = player1.card_list[i]
            if card in player1.active_list:
                player1.active_list.remove(card)
            else:
                player1.active_list.append(card)
                if len(player1.active_list) > 2:
                    del player1.active_list[0]
    if in_rect(pos, (1580 - 90, 20, 90, 60)):
        if len(player1.active_list) < 2:
            tickf1 = 30
        else:
            tickf1 = 0         
            if choose == 0:
                choose = 0.5
                mode = 'phase2'
                player1.showc = player1.active_list.copy() # p2는 지금 받으면 안됨
            if choose == 1:
                tick = 0
                mode = 'result'
                player1.showc = [player1.common] + player1.showc + player1.active_list.copy()
                player1.active_list = [] # 왜 이걸 여기서 초기화 시키지?
                player2.showc = [player2.common] + player2.showc + player2.active_list.copy()
                player2.active_list = []

    return player1, player2, mode, choose, tick, tickf1