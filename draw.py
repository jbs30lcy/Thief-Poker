import pygame as pg
from pygame.locals import *
from obj import *
pg.init()

def Mblit(screen, surf, pos, poscon = 'MM'):
    x, y = pos
    r, c = poscon
    rect = surf.get_rect()
    rx = rect.width
    ry = rect.height
    if   r == 'T': y = y
    elif r == 'M': y = y - ry/2
    elif r == 'B': y = y - ry
    else: raise NameError('Wrong condition')
    if   c == 'L': x = x
    elif c == 'M': x = x - rx/2
    elif c == 'R': x = x - rx
    else: raise NameError('Wrong condition')

    screen.blit(surf, (x, y))

AR72 = pg.font.SysFont('Arialrounded', 72)
AR24 = pg.font.SysFont('Arialrounded', 24)
AR36 = pg.font.SysFont('Arialrounded', 36)

Next_Button = pg.Surface((90, 60))
Next_Button.fill((227, 181, 140))
Next_Button_text = AR24.render('Next', True, Black)
Mblit(Next_Button, Next_Button_text, (45, 30))

def draw_play(screen, const, var):
    Round   = const[0]
    choose  = const[1]
    player1 = var[0]
    player2 = var[1]
    c1      = len(player1.card_list)

    screen.fill(Grey1)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)

    if choose == 1:
        text = AR72.render("Choose another two cards", True, Black)
    else:
        text = AR72.render("Choose two cards", True, Black) # choose == 0 or 0.5
    
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img, (x, 450), 'TM')
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x - 90, 450, 180, 270), 2)
        if card in player1.showc:
            pg.draw.rect(Alpha_screen, GreyA, (x - 90, 450, 180, 270))
    
    for i in range(4):
        if i < len(player2.showc):
            card = player2.showc[i]
            Mblit(screen, Card.shrink(card.img), (650 + i*100, 400), 'BM')
        else:
            Mblit(screen, Card.shrink(Card_IMGlist["Hide"]), (650 + i*100, 400), 'BM')

    Mblit(screen, text, (800, 100))
    Mblit(screen, Next_Button, (1300, 750), 'TR')
    
    text = AR24.render(f"round {Round}", True, Black)
    screen.blit(text, (20, 20))
    screen.blit(Alpha_screen, (0, 0))

    return (player1, player2)


def draw_flop(screen, const):
    player1 = const[0]
    player2 = const[1]

    screen.fill(Grey1)
    p1_text = AR24.render('My Card', True, Black)
    p2_text = AR24.render('Rival\'s Card', True, Black)
    Mblit(screen, player1.showc[0].img, (700, 480), 'TM')
    Mblit(screen, player1.showc[1].img, (900, 480), 'TM')
    Mblit(screen, player2.showc[0].img, (700, 420), 'BM')
    Mblit(screen, player2.showc[1].img, (900, 420), 'BM')
    Mblit(screen, p1_text, (1050, 530), 'TL')
    Mblit(screen, p2_text, (1050, 370), 'BL')


def draw_result(screen, const, var):
    w       = const
    player1 = var[0]
    player2 = var[1]
    tick    = var[2]

    screen.fill(Grey1)
    p1_text = AR24.render(f'My Card : {player1.rank()}', True, Black)
    p2_text = AR24.render(f'Rival\'s Card : {player2.rank()}', True, Black)
    for i in range(4):
        Mblit(screen, player1.showc[i].img, (500 + 200*i, 480), 'TM')
        Mblit(screen, player2.showc[i].img, (500 + 200*i, 420), 'BM')
    Mblit(screen, p1_text, (800, 760), 'TM')
    Mblit(screen, p2_text, (800, 140), 'BM')

    if w >= 0: # tick < 60 에서 w = -1로, 표기되지 않음.
        if w == 0:
            rtext = AR36.render(f'DRAW', True, Black)
            player1.coin += 10
        if w == 1:
            rtext = AR36.render(f'YOU WIN', True, Black)
            player1.coin += 5
        if w == 2:
            rtext = AR36.render(f'YOU LOSE', True, Black)
        Mblit(screen, rtext, (800, 840))

    return player1, player2, tick+1

def draw_exchange(screen, const, var):
    choose  = const
    player1 = var[0]
    player2 = var[1]
    c1      = len(player1.card_list)
    s2      = len(player2.shown)

    if choose == 1:
        text = AR72.render("Choose a card you want", True, Black)
    else:
        text = AR72.render("Choose my card", True, Black)

    screen.fill(Grey1)
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img, (x, 450), 'TM')
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x - 90, 450, 180, 270), 2)
    
    if choose == 1:
        for i in range(s2):
            card2 = player2.shown[i]
            x = 900 - s2*100 + i*200
            Mblit(screen, card2.img, (x, 400), 'BM')
            if card2 in player2.active_list:
                pg.draw.rect(screen, Red, (x - 90, 400 - 270, 180, 270), 2)
    Mblit(screen, text, (800, 70))
    Mblit(screen, Next_Button, (1300, 750), 'TR')

    return (player1, player2)


def draw_exchange_result(screen, const, var):
    player1 = const
    t = var
    c1 = len(player1.card_list)

    screen.fill(Grey1)
    text = AR72.render("Result", True, Black)
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img, (x, 450), 'TM')
    Mblit(screen, text, (800, 100))
    Mblit(screen, Next_Button, (1300, 750), 'TR')

    return t+1

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")