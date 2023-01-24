import pygame as pg
from pygame.locals import *
from obj import *
from moving import *
import math
pg.init()

bg1 = pg.transform.scale(pg.image.load(img_dir_path + 'com_bg.png'), (1600, 900))
bg2 = pg.transform.scale(pg.image.load(img_dir_path + 'com_bg_2.png'), (1600, 900))

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

NS = [pg.font.Font(file_path + '\\NanumSquareNeoOTF-cBd.otf', x) for x in range(1, 100)]
NSE = [pg.font.Font(file_path + '\\NanumSquareNeoOTF-dEb.otf', x) for x in range(1, 100)]
NS.insert(0, 0)
NSE.insert(0, 0)

Next_button = pg.transform.scale(pg.image.load(img_dir_path + 'Next_button.png'), (90, 60))
Rank_button = pg.transform.scale(pg.image.load(img_dir_path + 'Rank_button.png'), (90, 60))
Coin_icon = pg.transform.scale(pg.image.load(img_dir_path + 'coin.png'), (50, 50))

def n_draw_main(screen):
    screen.blit(bg1, (0, 0))

    title = NSE[96].render("도둑   포커", True, White)
    start_text = NS[56].render("게임   시작", True, Black)
    
    Mblit(screen, title, (800, 250))
    pg.draw.rect(screen, Brown1, (600, 600, 400, 100))
    Mblit(screen, start_text, (800, 650))
    
def n_draw_choose_key(screen, const, var):
    p1 = const
    tickf1, tickf2 = var

    class_val = p1.key // 10
    team_val  = p1.key % 10

    title = NS[80].render("반과  팀을  선택하세요", True, Black)
    class_text = NS[48].render("반", True, Black)
    team_text = NS[48].render("팀", True, Black)
    class_val_text = NSE[72].render(str(class_val), True, (8*tickf1, 26/30*tickf1, 0))
    team_val_text = NSE[72].render(str(team_val), True,   (8*tickf2, 26/30*tickf2, 0))

    screen.fill(Grey1)
    Mblit(screen, title, (800, 100))
    Mblit(screen, class_text, (400, 700))
    Mblit(screen, team_text, (1200, 700))
    Mblit(screen, class_val_text, (400, 450))
    Mblit(screen, team_val_text, (1200, 450))
    Mblit(screen, Next_button, (1350, 750))

    pg.draw.polygon(screen, Red, [(400, 360), (380, 370), (420, 370)])
    pg.draw.polygon(screen, Red, [(400, 540), (380, 530), (420, 530)])
    pg.draw.polygon(screen, Red, [(1110, 450), (1120, 430), (1120, 470)])
    pg.draw.polygon(screen, Red, [(1290, 450), (1280, 430), (1280, 470)])

    if tickf1: tickf1 -= 1
    if tickf2: tickf2 -= 1
    return tickf1, tickf2

def n_draw_play_pre(screen, const, var):
    player1, player2 = const
    tick = var

    c1 = len(player1.card_list)

    screen.blit(bg2, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x0 = 850 - c1*50
        if tick <= 5:
            x, y = x0, 1115
        if 5 < tick <= 20:
            x, y = easing((x0, 1115), (x0, 700), m_quadout, tick-5, 15)
        if 20 < tick <= 30:
            x, y = x0, 700
        if 30 < tick <= 45:
            x, y = easing((x0, 700), (x0 + i*100, 700), m_quadinout, tick-30, 15)
        if 45 < tick <= 60:
            x, y = x0 + i*100, 700
        Mblit(screen, card.img_half, (x, y))

    return tick+1

def n_draw_play(screen, const, var):
    Round, Match, choose, tickf1 = const
    player1, player2, tick = var

    c1 = len(player1.card_list)
    c2 = len(player2.card_list)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)

    if choose == 0 or choose == 0.5:
        title = NS[72].render("카드 두 장을 선택하세요", True, White)
    if choose == 1:
        title = NS[72].render("다른 카드 두 장을 선택하세요", True, White)
    Match_text = NS[24].render(f'Match {Match}', True, White)
    Round_text = NS[24].render(f'Round {Round}', True, White)
    team_text = NSE[48].render(str(player2.key%10), True, Black)
    warn_text = NSE[72].render('Choose more card.', True, Black).convert_alpha()
    warn_text.set_alpha(tickf1*255/30)

    screen.blit(bg2, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x, y = 850 - c1*50 + 100*i, 700
        Mblit(screen, card.img_half, (x, y))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x-150, y-225, 300, 450), 4, border_radius = 30)
    for i in range(c2):
        card = player2.card_list[i]
        x, y = 816.6 - c1*16.7 + 33.3*i, 300
        Mblit(screen, Card.shrink(CI_ori['Hide'], 1/6), (x, y))
    Mblit(screen, title, (800, 80))
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Round_text, (20, 55), 'TL')
    Mblit(screen, Next_button, (1580, 20), 'TR')

    pg.draw.rect(screen, Grey1, (150, 280, 210, 40))
    pg.draw.circle(screen, White, (150, 300), 50)
    Mblit(screen, team_text, (150, 300))
    Mblit(Alpha_screen, warn_text, (800, 450))

    screen.blit(Alpha_screen, (0, 0))

    return player1, player2, tick+1
