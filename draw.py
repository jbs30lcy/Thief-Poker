# draw.py : 플레이어들에게 보여지는 UI를 그리는 부분을 떼어놓은 파일.
import pygame as pg
from pygame.locals import *
from obj import *
import math
pg.init()

# Mblit : ~~.blit 메소드는 입력받은 좌표를 왼쪽 위로 설정하고 Surface를 그림.
# 그 좌표의 기준을 정할 수 있는 함수
# 기본값은 MM, 즉 입력 좌표를 정중앙으로 두게끔 그림.
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

# 글꼴은 일단 Arialrounded를 썼지만, 이 글꼴은 한글이 호환되지 않는다.
AR = [pg.font.SysFont('Arialrounded', x) for x in range(1, 100)]
AR.insert(0, 0)

Next_Button = pg.Surface((90, 60))
Next_Button.fill(Brown1)
Next_Button_text = AR[24].render('Next', True, Black)
Mblit(Next_Button, Next_Button_text, (45, 30))

Coin_icon = pg.transform.scale(pg.image.load(img_dir_path + 'coin.png'), (50, 50))


# draw_begin : mode = start일 때의 UI
def draw_begin(screen): 
    screen.fill(Grey1)

    title = AR[96].render("Dodook Poker", True, Black)
    start_button = pg.Surface((300, 100))
    start_button.fill(Brown1)
    start_button_text = AR[48].render('Start', True, Black)
    Mblit(start_button, start_button_text, (150, 50))

    Mblit(screen, title, (800, 150))
    Mblit(screen, start_button, (800, 700))

# draw_getmatch : mode = getMatch일 떄의 UI
def draw_getmatch(screen, var):
    tick = var

    screen.fill(Grey1)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    text = AR[72].render("Finding player...", True, Black)
    Mblit(screen, text, (800, 150))

    for i in range(8):
        x = 800 + 120*math.sin(math.pi * (i + round(tick/5)) / 4)
        y = 450 + 120*math.cos(math.pi * (i + round(tick/5)) / 4)
        c = list(Green) + [55 + i*200 / 8]
        pg.draw.circle(Alpha_screen, c, (x, y), 20)

    screen.blit(Alpha_screen, (0, 0))
    return tick+1


# draw_play : mode = play일 때의 UI
def draw_play(screen, const, var):
    Round   = const[0]
    choose  = const[1]
    player1 = var[0]
    player2 = var[1]
    c1      = len(player1.card_list)

    screen.fill(Grey1)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)

    if choose == 1:
        text = AR[72].render("Choose another two cards", True, Black)
    else:
        text = AR[72].render("Choose two cards", True, Black) # choose == 0 or 0.5
    
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
    
    text = AR[24].render(f"round {Round}", True, Black)
    coin = AR[24].render(str(player1.coin), True, Black)
    coin_icon_x = 1580 - coin.get_width()
    Mblit(screen, text, (20, 20), 'TL')
    Mblit(screen, coin, (1580, 40), 'MR')
    Mblit(screen, Coin_icon, (coin_icon_x - 10, 40), 'MR')
    screen.blit(Alpha_screen, (0, 0))

    return (player1, player2)


# draw_flop : mode = phase2일 떄의 UI
def draw_flop(screen, const):
    Round   = const[0]
    player1 = const[1]
    player2 = const[2]

    screen.fill(Grey1)
    p1_text = AR[24].render('My Card', True, Black)
    p2_text = AR[24].render('Rival\'s Card', True, Black)
    Mblit(screen, player1.showc[0].img, (700, 480), 'TM')
    Mblit(screen, player1.showc[1].img, (900, 480), 'TM')
    Mblit(screen, player2.showc[0].img, (700, 420), 'BM')
    Mblit(screen, player2.showc[1].img, (900, 420), 'BM')
    Mblit(screen, p1_text, (1050, 530), 'TL')
    Mblit(screen, p2_text, (1050, 370), 'BL')

    text = AR[24].render(f"round {Round}", True, Black)
    coin = AR[24].render(str(player1.coin), True, Black)
    coin_icon_x = 1580 - coin.get_width()
    Mblit(screen, text, (20, 20), 'TL')
    Mblit(screen, coin, (1580, 40), 'MR')
    Mblit(screen, Coin_icon, (coin_icon_x - 10, 40), 'MR')
    Mblit(screen, Next_Button, (1300, 750), 'TR')


# draw_result : mode = result일 때의 UI
def draw_result(screen, const, var):
    Round   = const[0]
    w       = const[1]
    player1 = var[0]
    player2 = var[1]
    tick    = var[2]

    screen.fill(Grey1)
    p1_text = AR[24].render(f'My Card : {player1.rank()}', True, Black)
    p2_text = AR[24].render(f'Rival\'s Card : {player2.rank()}', True, Black)
    for i in range(4):
        Mblit(screen, player1.showc[i].img, (500 + 200*i, 480), 'TM')
        Mblit(screen, player2.showc[i].img, (500 + 200*i, 420), 'BM')
    Mblit(screen, p1_text, (800, 760), 'TM')
    Mblit(screen, p2_text, (800, 140), 'BM')

    if w >= 0: # tick < 60 에서 w = -1로, 표기되지 않음.
        if w == 0:
            rtext = AR[36].render(f'DRAW', True, Black)
            if tick == 60: player1.coin += 5
        if w == 1:
            rtext = AR[36].render(f'YOU WIN', True, Black)
            if tick == 60: player1.coin += 10
        if w == 2:
            rtext = AR[36].render(f'YOU LOSE', True, Black)
        Mblit(screen, rtext, (800, 840))

    text = AR[24].render(f"round {Round}", True, Black)
    coin = AR[24].render(str(player1.coin), True, Black)
    coin_icon_x = 1580 - coin.get_width()
    Mblit(screen, text, (20, 20), 'TL')
    Mblit(screen, coin, (1580, 40), 'MR')
    Mblit(screen, Coin_icon, (coin_icon_x - 10, 40), 'MR')
    if tick >= 60: Mblit(screen, Next_Button, (1450, 750), 'TR')

    return player1, player2, tick+1


# draw_exchange : mode = exchange일 때의 UI
def draw_exchange(screen, const, var):
    choose  = const
    player1 = var[0]
    player2 = var[1]
    c1      = len(player1.card_list)
    s2      = len(player2.shown)

    if choose == 1:
        text = AR[72].render("Choose a card you want", True, Black)
    else:
        text = AR[72].render("Choose my card", True, Black)

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

# draw_exchange_result : mode = exchangeR일 때의 UI
def draw_exchange_result(screen, const, var):
    player1 = const
    t = var
    c1 = len(player1.card_list)

    screen.fill(Grey1)
    text = AR[72].render("Result", True, Black)
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img, (x, 450), 'TM')
    Mblit(screen, text, (800, 100))
    Mblit(screen, Next_Button, (1300, 750), 'TR')

    return t+1

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")