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

Next_Button = pg.Surface((90, 60))
Next_Button.fill(Brown1)
Next_Button_text = NS[24].render('Next', True, Black)
Mblit(Next_Button, Next_Button_text, (45, 30))

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
    Mblit(screen, Next_Button, (1350, 750))

    pg.draw.polygon(screen, Red, [(400, 360), (380, 370), (420, 370)])
    pg.draw.polygon(screen, Red, [(400, 540), (380, 530), (420, 530)])
    pg.draw.polygon(screen, Red, [(1110, 450), (1120, 430), (1120, 470)])
    pg.draw.polygon(screen, Red, [(1290, 450), (1280, 430), (1280, 470)])

    if tickf1: tickf1 -= 1
    if tickf2: tickf2 -= 1
    return tickf1, tickf2