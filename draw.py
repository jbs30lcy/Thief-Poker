# draw.py : 플레이어들에게 보여지는 UI를 그리는 부분을 떼어놓은 파일.
import pygame as pg
from pygame.locals import *
from obj import *
import math
pg.init()

bg1 = pg.transform.scale(pg.image.load(img_dir_path + 'com_bg.png'), (1600, 900)) # 테이블 앞 배경
bg2 = pg.transform.scale(pg.image.load(img_dir_path + 'com_bg.png'), (1600, 900)) # 테이블 뒤 배경

# in_rect: 점이 사각형 안에 포함되어 있으면 True를 return
def in_rect(pos, rect):
    return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]

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

NS = [pg.font.Font(file_path + '\\NanumSquareNeoOTF-cBd.otf', x) for x in range(1, 100)]
NSE = [pg.font.Font(file_path + '\\NanumSquareNeoOTF-dEb.otf', x) for x in range(1, 100)]
NS.insert(0, 0)
NSE.insert(0, 0)

Next_Button = pg.Surface((90, 60))
Next_Button.fill(Brown1)
Next_Button_text = NS[24].render('Next', True, Black)
Mblit(Next_Button, Next_Button_text, (45, 30))

Coin_icon = pg.transform.scale(pg.image.load(img_dir_path + 'coin.png'), (50, 50))


# draw_begin : mode = start일 때의 UI
def draw_begin(screen): 
    screen.blit(bg1, (0, 0))

    title = NSE[96].render("도둑 포커", True, Black)
    start_button = pg.Surface((300, 100))
    start_button.fill(Brown1)
    start_button_text = NS[48].render('Start', True, Black)
    Mblit(start_button, start_button_text, (150, 50))

    Mblit(screen, title, (800, 250))
    Mblit(screen, start_button, (800, 640))


# draw_chooserank : mode = chooseRank일 때의 UI
def draw_chooserank(screen, const):
    r1  = const[0][0]
    r2  = const[0][1]
    pos = const[1]
    
    screen.fill(Grey1)

    Straight = pg.Surface((200, 120))
    Flush    = pg.Surface((200, 120))
    NoDD     = pg.Surface((200, 120))
    oneDD    = pg.Surface((200, 120))
    twoDD    = pg.Surface((200, 120))
    fourDD   = pg.Surface((200, 120))
    Straight.fill(Grad2)
    Flush.fill(Grad3)
    NoDD.fill(Grad1)
    oneDD.fill(Grad2)
    twoDD.fill(Grad3)
    fourDD.fill(Grad4)
    Mblit(Straight, NS[36].render('Straight', True, Black),     (100, 60))
    Mblit(Flush,    NS[36].render('Flush', True, Black),        (100, 60))
    Mblit(NoDD,     NS[27].render('No DDangjabi', True, Black), (100, 60))
    Mblit(oneDD,    NS[36].render('type I', True, Black),       (100, 60))
    Mblit(twoDD,    NS[36].render('type II', True, Black),      (100, 60))
    Mblit(fourDD,   NS[36].render('type III', True, Black),     (100, 60))

    text = NS[60].render('Choose one', True, Black)
    Mblit(screen, text,     (800, 100))
    Mblit(screen, Straight, (550, 200), 'TL')
    Mblit(screen, Flush,    (850, 200), 'TL')

    text = NS[60].render('Choose DDangjabi', True, Black)
    Mblit(screen, text,   (800, 500))
    Mblit(screen, NoDD,   (250, 600), 'TL')
    Mblit(screen, oneDD,  (550, 600), 'TL')
    Mblit(screen, twoDD,  (850, 600), 'TL')
    Mblit(screen, fourDD, (1150, 600), 'TL')

    if in_rect(pos, (550, 600, 200, 120)):
        desc = f"If the rank is 'No Rank' and it contains certain card(randomly selected), it will beat {r1}."
    elif in_rect(pos, (850, 600, 200, 120)):
        desc = f"If the rank is 'One Pair' and their colors are same as certain colors(randomly selected), it will beat {r1}."
    elif in_rect(pos, (1150, 600, 200, 120)):
        desc = f"If the rank is lower than 'One Pair' and contains all four colors, it will beat {r1}."
    else:
        desc = ''
    desc_surf = NS[28].render(desc, True, Black)
    Mblit(screen, desc_surf, (800, 850))

    if r1 == 'Straight': pg.draw.rect(screen, Red, (550, 200, 200, 120), 3)
    if r1 == 'Flush':    pg.draw.rect(screen, Red, (850, 200, 200, 120), 3)
    
    if not r2:  pg.draw.rect(screen, Red, (250, 600, 200, 120), 3)
    if 1 in r2: pg.draw.rect(screen, Red, (550, 600, 200, 120), 3)
    if 2 in r2: pg.draw.rect(screen, Red, (850, 600, 200, 120), 3)
    if 4 in r2: pg.draw.rect(screen, Red, (1150, 600, 200, 120), 3)

    Mblit(screen, Next_Button, (1300, 450))


# draw_showDD : mode = showDD일 떄의 UI
def draw_showDD(screen, const, var):
    dd   = const
    tick = var

    screen.fill(Grey1)
    screen.blit(bg1, (0, 0))

    if dd[0]:
        text = NS[40].render('DDangjabi Card', True, Black)
        Mblit(screen, text, (400, 300))
        Mblit(screen, dd[0].img, (400, 500))
    if dd[1]:
        text = NS[40].render('DDangjabi Color', True, Black)
        Mblit(screen, text, (1200, 300))
        pg.draw.rect(screen, eval(dd[1][0]), (1010, 500 - 135, 180, 270))
        pg.draw.rect(screen, eval(dd[1][1]), (1210, 500 - 135, 180, 270))
        pg.draw.rect(screen, White, (1010, 500 - 135, 180, 270), 3)
        pg.draw.rect(screen, White, (1210, 500 - 135, 180, 270), 3)
        Mblit(screen, NS[48].render(dd[1][0], True, Black), (1100, 500))
        Mblit(screen, NS[48].render(dd[1][1], True, Black), (1300, 500))
    
    return tick+1


# draw_getmatch : mode = getMatch일 떄의 UI
def draw_getmatch(screen, var):
    tick = var

    screen.fill(Grey1)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    text = NS[72].render("Finding player...", True, Black)
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
    Match   = const[1]
    choose  = const[2]
    player1 = var[0]
    player2 = var[1]
    c1      = len(player1.card_list)

    screen.blit(bg2, (0, 0))
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)

    if choose == 1:
        text = NS[72].render("Choose another two cards", True, White)
    else:
        text = NS[72].render("Choose two cards", True, White) # choose == 0 or 0.5
    
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

    if choose == 1:
        Mblit(screen, Card.shrink(player1.common.img), (1200, 400), 'BM')
        pg.draw.rect(screen, Yellow, (1200 - 50, 400 - 140, 100, 145), 2)
    
    Mblit(screen, text, (800, 100))
    Mblit(screen, Next_Button, (1300, 750), 'TR')
    
    if 1 in player1.Rule[1]:
        DD_text = NS[28].render('땡잡이 카드', True, White)
        Mblit(screen, DD_text, (150, 220))
        Mblit(screen, Card.shrink(player1.dd[0].img), (150, 250), 'TM')
    if 2 in player1.Rule[1]:
        DD_text = NS[28].render('땡잡이 색', True, White)
        Mblit(screen, DD_text, (1450, 220))
        pg.draw.rect(screen, player1.dd[1][0], (1400, 250, 50, 75))
        pg.draw.rect(screen, player1.dd[1][1], (1450, 250, 50, 75))
        
    
    Match_text = NS[24].render(f"Match {Match}", True, White)
    Round_text = NS[24].render(f"round {Round}", True, White)
    coin = NS[24].render(str(player1.coin), True, White)
    coin_icon_x = 1580 - coin.get_width()
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Round_text, (20, 50), 'TL')
    Mblit(screen, coin, (1580, 40), 'MR')
    Mblit(screen, Coin_icon, (coin_icon_x - 10, 40), 'MR')

    screen.blit(Alpha_screen, (0, 0))
    return (player1, player2)


# draw_flop : mode = phase2일 떄의 UI
def draw_flop(screen, const, var):
    Round   = const[0]
    Match   = const[1]
    player1 = const[2]
    player2 = const[3]
    tick    = var

    screen.blit(bg1, (0, 0))
    p1_text = NS[28].render('My Card', True, White)
    p2_text = NS[28].render('Rival\'s Card', True, White)
    Mblit(screen, player1.showc[0].img, (700, 480), 'TM')
    Mblit(screen, player1.showc[1].img, (900, 480), 'TM')
    Mblit(screen, player2.showc[0].img, (700, 420), 'BM')
    Mblit(screen, player2.showc[1].img, (900, 420), 'BM')
    Mblit(screen, p1_text, (1050, 530), 'TL')
    Mblit(screen, p2_text, (1050, 370), 'BL')

    Match_text = NS[24].render(f"Match {Match}", True, White)
    Round_text = NS[24].render(f"round {Round}", True, White)
    coin = NS[24].render(str(player1.coin), True, White)
    coin_icon_x = 1580 - coin.get_width()
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Round_text, (20, 50), 'TL')
    Mblit(screen, coin, (1580, 40), 'MR')
    Mblit(screen, Coin_icon, (coin_icon_x - 10, 40), 'MR')
    if tick >= 60:
        text = NS[28].render('Community card', True, White)
        Mblit(screen, text, (300, 270))
        Mblit(screen, Next_Button, (1300, 750), 'TR')
        Mblit(screen, player1.common.img, (300, 450))

    return tick+1


# draw_result : mode = result일 때의 UI
def draw_result(screen, const, var):
    Round   = const[0]
    Match   = const[1]
    w       = const[2]
    player1 = var[0]
    player2 = var[1]
    tick    = var[2]

    screen.blit(bg1, (0, 0))
    if tick >= 60:
        if ('Straight' in player1.rank() or 'Flush' in player1.rank()) and player2.isdd: p2s = 'DDangjabi!'
        else: p2s = player2.rank()
        if ('Straight' in player2.rank() or 'Flush' in player2.rank()) and player1.isdd: p1s = 'DDangjabi!'
        else: p1s = player1.rank()
    else:
        p1s = player1.rank()
        p2s = player2.rank()
    p1_text = NS[24].render(f'My Card : {p1s}', True, White)
    p2_text = NS[24].render(f'Rival\'s Card : {p2s}', True, White)
    for i in range(5):
        Mblit(screen, player1.showc[i].img, (400 + 200*i, 480), 'TM')
        Mblit(screen, player2.showc[i].img, (400 + 200*i, 420), 'BM')
    pg.draw.rect(screen, Yellow, (400 - 95, 480 - 5, 190, 280), 2)
    pg.draw.rect(screen, Yellow, (400 - 95, 420 - 275, 190, 280), 2)
    Mblit(screen, p1_text, (800, 780), 'TM')
    Mblit(screen, p2_text, (800, 120), 'BM')

    if w >= 0: # tick < 60 에서 w = -1로, 표기되지 않음.
        if w == 0:
            rtext = NS[36].render(f'DRAW', True, White)
            if tick == 60: player1.coin += 5
        if w == 1:
            rtext = NS[36].render(f'YOU WIN', True, White)
            if tick == 60: player1.coin += 10
        if w == 2:
            rtext = NS[36].render(f'YOU LOSE', True, White)
        Mblit(screen, rtext, (800, 840))


    Match_text = NS[24].render(f"Match {Match}", True, White)
    Round_text = NS[24].render(f"round {Round}", True, White)
    coin = NS[24].render(str(player1.coin), True, White)
    coin_icon_x = 1580 - coin.get_width()
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Round_text, (20, 50), 'TL')
    Mblit(screen, coin, (1580, 40), 'MR')
    Mblit(screen, Coin_icon, (coin_icon_x - 10, 40), 'MR')
    if tick >= 60: Mblit(screen, Next_Button, (1450, 750), 'TR')

    return player1, player2, tick+1


# draw_exchange : mode = exchange일 때의 UI
def draw_exchange(screen, const, var):
    Match   = const[0]
    choose  = const[1]
    player1 = var[0]
    player2 = var[1]
    c1      = len(player1.card_list)
    s2      = len(player2.shown)

    if choose == 1:
        text = NS[72].render("Choose a card you want", True, White)
    else:
        text = NS[72].render("Choose my card", True, White)

    screen.blit(bg1, (0, 0))
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

    Match_text = NS[24].render(f"Match {Match}", True, White)
    Mblit(screen, Match_text, (20, 20), 'TL')

    return (player1, player2)

# draw_exchange_result : mode = exchangeR일 때의 UI
def draw_exchange_result(screen, const, var):
    Match   = const[0]
    player1 = const[1]
    t       = var
    c1 = len(player1.card_list)

    screen.blit(bg1, (0, 0))
    text = NS[72].render("Result", True, White)
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img, (x, 450), 'TM')
    Mblit(screen, text, (800, 100))
    Mblit(screen, Next_Button, (1300, 750), 'TR')

    Match_text = NS[24].render(f"Match {Match}", True, White)
    Mblit(screen, Match_text, (20, 20), 'TL')

    return t+1

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")