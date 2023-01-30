import pygame as pg
from pygame.locals import *
from obj import *
from setting import *
pg.init()
NUMBER_OF_GROUPS = 26
NUMBER_OF_TEAMS = 8

def mouse_main(var):
    mode, player1 = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)
    if in_rect(pos, (600, 600, 400, 100)):
        mode = 'choose_key'
        player1.group = 1
        player1.team = 1
    
    return mode

def key_choose_key(const, var):
    event = const
    player1, tickf1, tickf2 = var

    if event.key == K_UP:
        player1.group = player1.group % NUMBER_OF_GROUPS + 1
        tickf1 = 30
        
    if event.key == K_DOWN:
        player1.group -= 2 
        player1.group %= NUMBER_OF_GROUPS
        player1.group += 1
        tickf1 = 30
    if event.key == K_RIGHT:
        player1.team %= NUMBER_OF_TEAMS
        player1.team += 1 
        tickf2 = 30
        
    if event.key == K_LEFT:
        player1.team -= 2
        player1.team %= NUMBER_OF_TEAMS
        player1.team += 1 
        tickf2 = 30
    return player1, tickf1, tickf2

def mouse_choose_key(var):
    mode = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)
    if in_rect(pos, (1350-45, 750-30, 90, 60)):
        mode = 'get_match'

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
                player1.showc = player1.active_list.copy()
                #player2.showc = player2.active_list.copy()
                player1.set_shown()
                player2.set_shown()
                tick = -1                
                mode = 'flop_pre'
            if choose == 1:
                tick = -1
                mode = 'flop_pre'
                player1.showc = player1.showc + player1.active_list.copy()
                
                #player2.showc = player2.showc + player2.active_list.copy()
                

    return player1, player2, mode, choose, tick, tickf1

def mouse_flop(var):
    mode, player1, player2, tick = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)

    if in_rect(pos, (1580 - 90, 20, 90, 60)):
        tick = -1
        player1, player2 = phase2((player1, player2))
        mode = 'play'

    return mode, player1, player2, tick

def mouse_result(var):
    mode, Round, tick, choose, player1, player2 = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)

    if tick >= 70 and in_rect(pos, (1580 - 90, 20, 90, 60)):
        Round += 1
        mode = 'reset'
        if Round == 3:
            Round = 1
            choose = 0
            tick = -1
            player1.active_list = []
            player2.active_list = []
            player1.showc = []
            player2.showc = []
            if sum(player1.pre[-1]) > 0: mode = 'exchange_delay'
            if sum(player1.pre[-1]) == 0: mode = 'exchange_draw'
            if sum(player1.pre[-1]) < 0: mode = 'exchange_lose'

    return mode, Round, tick, choose, player1, player2

def mouse_exchange_lose(var):
    mode, choose, tickf1, player1, player2 = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)

    c1 = len(player1.card_list)
    s2 = len(player2.shown)
    print(f"MOUSE_EXCHANGE_LOSE : \nc1 {player1.card_list}\ns2 {player2.shown}")
    if choose == 0:
        for i in range(c1):
            x = 900 - c1*100 + i*200
            if in_rect(pos, (x - 90, 480, 180, 270)):
                card = player1.card_list[i]
                if card in player1.active_list:
                    player1.active_list.remove(card)
                else:
                    player1.active_list.append(card)
                    if len(player1.active_list) > 1:
                        del player1.active_list[0]
        if in_rect(pos, (1580 - 90, 20, 90, 60)):
            if len(player1.active_list) < 1:
                tickf1 = 30
            else:
                tickf1 = 0
                choose = 0.5
    
    if choose == 1:
        for i in range(s2):
            x = 900 - s2*100 + i*200
            if in_rect(pos, (x - 90, 150, 180, 270)):
                card = player2.shown[i]
                if card in player2.active_list:
                    player2.active_list.remove(card)
                else:
                    player2.active_list.append(card)
                    if len(player2.active_list) > 1:
                        del player2.active_list[0]

        if in_rect(pos, (1580 - 90, 20, 90, 60)):
            if len(player2.active_list) < 1:
                tickf1 = 30
            else:
                tickf1 = 0
                choose = 0
                mode = 'exchange_result'

                player1.ex_index = player1.card_list.index(player1.active_list[0])
                player1.ex_card = player1.active_list[0]
                i = 0
                while i < len(player2.card_list): #equals 로 교체 필요
                    if str(player2.card_list[i]) == str(player2.active_list[0]):
                        player2.ex_index = i 
                        break
                    i+=1
                player2.ex_card = player2.active_list[0]

    return mode, choose, tickf1, player1, player2

def mouse_exchange_draw(var):
    mode, tick, tickf1, player1, player2 = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)

    s2 = len(player2.shown)
    for i in range(s2):
        x = 900 - s2*100 + i*200
        if in_rect(pos, (x - 90, 420 - 270, 180, 270)):
            card = player2.shown[i]
            if card in player2.active_list:
                player2.active_list.remove(card)
            else:
                player2.active_list.append(card)
                if len(player2.active_list) > 1:
                    del player2.active_list[0]
    if in_rect(pos, (1580 - 90, 20, 90, 60)):
        if len(player2.active_list) < 1:
            tickf1 = 30
        else:
            tickf1 = 0
            tick = 0
            player2.ex_card = player2.active_list[0]
            mode = 'exchange_delay'

    return mode, tick, tickf1, player1, player2

def mouse_exchange_result(var):
    mode, tick = var

    pos = list(pg.mouse.get_pos())
    pos[0] *= (1600/WIDTH)
    pos[1] *= (900/HEIGHT)

    if in_rect(pos, (1580 - 90, 20, 90, 60)):
        tick = -1
        mode = 'get_match'

    return mode, tick