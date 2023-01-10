import pygame as pg
from pygame.locals import *
import sys
from obj import *

pg.init()
AR72 = pg.font.SysFont('Arialrounded', 72)
AR24 = pg.font.SysFont('Arialrounded', 24)
AR36 = pg.font.SysFont('Arialrounded', 36)

Next_Button = pg.Surface((90, 60))
Next_Button.fill((227, 181, 140))
Next_Button_text = AR24.render('Next', True, Black)
Next_Button.blit(Next_Button_text, (18, 15))

def draw_play(screen, const, var):
    Round   = const[0]
    choose  = const[1]
    player1 = var[0]
    player2 = var[1]

    screen.fill(Grey1)
    Alpha_screen = pg.Surface((1200, 900), pg.SRCALPHA)
    if choose == 0:
        text = AR72.render("Choose two cards", True, Black)
        for i in range(6):
            card = player1.card_list[i]
            screen.blit(card.img, (10 + i*200, 450))
            if card in player1.active_list:
                pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
        for i in range(4):
            screen.blit(Card.shrink(Card_IMGlist["Hide"]), ((400 + i*100, 300)))
        screen.blit(text, (300, 50))
        screen.blit(Next_Button, (800, 750))
    
    if choose == 1:
        text = AR72.render("Choose another two cards", True, Black)
        for i in range(6):
            card = player1.card_list[i]
            screen.blit(card.img, (10 + i*200, 450))
            if card in player1.active_list:
                pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
            if card in player1.showc:
                pg.draw.rect(Alpha_screen, GreyA, (10 + i*200, 450, 180, 270))
        for i in range(4):
            if i < len(player2.showc):
                card = player2.showc[i]
                screen.blit(Card.shrink(card.img), (400 + i*100, 300))
            else:
                screen.blit(Card.shrink(Card_IMGlist["Hide"]), ((400 + i*100, 300)))
        screen.blit(text, (150, 50))
        screen.blit(Next_Button, (800, 750))
    
    text = AR24.render(f"round {Round}", True, Black)
    screen.blit(text, (20, 20))
    screen.blit(Alpha_screen, (0, 0))

    return (player1, player2)


def draw_flop(screen, const):
    player1 = const[0]
    player2 = const[1]

    screen.fill(Grey1)
    for card in player1.showc:
        if not card in player1.shown:
            player1.shown.append(card)
    for card in player2.showc:
        if not card in player2.shown:
            player2.shown.append(card)
    player2.showc = player2.active_list.copy()

    screen.blit(player1.showc[0].img, (310, 450))
    screen.blit(player1.showc[1].img, (510, 450))
    screen.blit(player2.showc[0].img, (310, 150))
    screen.blit(player2.showc[1].img, (510, 150))
    p1_text = AR24.render('My Card', True, Black)
    p2_text = AR24.render('Rival\'s Card', True, Black)
    screen.blits([ (p1_text, (720, 600)) , (p2_text, (720, 300)) ])

def draw_result(screen, const, var):
    w       = const
    player1 = var[0]
    player2 = var[1]
    tick    = var[2]

    screen.fill(Grey1)
    for card in player1.showc:
        if not card in player1.shown:
            player1.shown.append(card)
    for card in player2.showc:
        if not card in player2.shown:
            player2.shown.append(card)
    for i in range(4):
        screen.blit(player1.showc[i].img, (110 + 200*i, 450))
        screen.blit(player2.showc[i].img, (110 + 200*i, 150))
    p1_text = AR24.render(f'My Card : {player1.rank()}', True, Black)
    p2_text = AR24.render(f'Rival\'s Card : {player2.rank()}', True, Black)
    screen.blits([ (p1_text, (400, 740)) , (p2_text, (400, 100)) ])

    if w >= 0:
        if w == 0:
            rtext = AR36.render(f'DRAW', True, Black)
            player1.coin += 10
        if w == 1:
            rtext = AR36.render(f'YOU WIN', True, Black)
            player1.coin += 5
        if w == 2:
            rtext = AR36.render(f'YOU LOSE', True, Black)
        wx = 600 - rtext.get_rect().width / 2
        screen.blit(rtext, (wx, 820))

    return player1, player2, tick+1

def draw_exchange(screen, const, var):
    choose  = const
    player1 = var[0]
    player2 = var[1]
    screen.fill(Grey1)
    if choose == 0:
        text = AR72.render("Choose my card", True, Black)
        for i in range(6):
            card = player1.card_list[i]
            screen.blit(card.img, (10 + i*200, 450))
            if card in player1.active_list:
                pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
        screen.blit(text, (300, 50))
        screen.blit(Next_Button, (800, 750))
    
    if choose == 1:
        text = AR72.render("Choose a card you want", True, Black)
        for i in range(6):
            card = player1.card_list[i]
            screen.blit(card.img, (10 + i*200, 450))
            if card in player1.active_list:
                pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
        for i in range(len(player2.shown)):
            card = player2.shown[i]
            screen.blit(card.img, (610 - 100 * len(player2.shown)+ i*200, 150))
            if card in player2.active_list:
                pg.draw.rect(screen, Red, (610 - 100 * len(player2.shown)+ i*200, 150, 180, 270), 2)
        screen.blit(text, (200, 50))
        screen.blit(Next_Button, (800, 750))

    return (player1, player2)


def draw_exchange_result(screen, const, var):
    player1 = const
    t = var

    screen.fill(Grey1)
    text = AR72.render("Result", True, Black)
    for i in range(len(player1.card_list)):
        card = player1.card_list[i]
        screen.blit(card.img, (10 + i*200, 450))
    screen.blit(text, (500, 50))
    screen.blit(Next_Button, (800, 750))

    return t+1

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")