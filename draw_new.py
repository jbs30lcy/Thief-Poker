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

def str2Kr(s):
    col_kr_dict = {'Red': '빨강', 'Blue': '파랑', 'Yellow': '노랑', 'Green': '초록'}
    blacks = '검은' if 'Black' in s else ''
    if 'Four of a kind' in s:
        return f'{blacks} {s[0]} 포카드'
    if 'Straight' in s:
        return f'{blacks} {s[0]} 스트레이트'
    if 'Flush' in s:
        i = s.find(' ')
        return f'{blacks} {col_kr_dict[s[:i]]} 플러시'
    if 'Three of a kind' in s:
        return f'{blacks} {s[0]} 트리플'
    if 'Two pair' in s:
        return f'{blacks} {s[:3]} 투 페어'
    if 'Pair' in s:
        return f'{blacks} {s[0]} 원 페어'
    return f'족보 없음 {s[8:]}'

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

def n_draw_get_match(screen, var):
    tick = var

    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    title = NS[72].render("Finding player...", True, Black)

    screen.fill(Grey1)
    Mblit(screen, title, (800, 150))
    for i in range(8):
        x = 800 + 120*math.sin(math.pi * (i + round(tick/5)) / 4)
        y = 450 + 120*math.cos(math.pi * (i + round(tick/5)) / 4)
        c = list(Green) + [55 + i*200 / 8]
        pg.draw.circle(Alpha_screen, c, (x, y), 20)

    screen.blit(Alpha_screen, (0, 0))
    return tick+1

def n_draw_play_pre(screen, const, var):
    player1, player2 = const
    tick = var
    
    screen.blit(bg2, (0, 0))
    c1 = len(player1.card_list)
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
    coin_text = NS[30].render(str(player1.coin), True, White)
    common_card = player1.common

    screen.blit(bg2, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x, y = 850 - c1*50 + 100*i, 700
        Mblit(screen, card.img_half, (x, y))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x-150, y-225, 300, 450), 4, border_radius = 30)
        if choose == 1 and card in player1.showc:
            pg.draw.rect(screen, Grey3, (x-150, y-225, 300, 450), 10, border_radius = 30)
    for i in range(c2):
        card = player2.card_list[i]
        x, y = 816.6 - c1*16.7 + 33.3*i, 300
        Mblit(screen, Card.shrink(CI_ori['Hide'], 1/6), (x, y))
    if choose == 1:
        Mblit(screen, common_card.img_ci, (1300, 300))
        pg.draw.rect(screen, Yellow, (1195, 150, 210, 300), 3, border_radius = 15)

    pg.draw.rect(screen, White, (150, 280, 210, 40))
    pg.draw.circle(screen, White, (150, 300), 50)
    for i in range(5):
        if Match < i+2: continue
        v = sum(player2.pre[-i-2])
        if v == 2: color = Green
        if v == 1: color = GreenG
        if v == 0: color = Grey4
        if v == -1: color = RedG
        if v == -2: color = Red
        pg.draw.rect(screen, color, (325 - 30*i, 285, 30, 30))
    
    Mblit(screen, title, (800, 80))
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Round_text, (20, 55), 'TL')
    Mblit(screen, Next_button, (1580, 20), 'TR')
    Mblit(screen, Coin_icon, (20, 855), 'ML')
    Mblit(screen, coin_text, (80, 855), 'ML')
    Mblit(screen, team_text, (150, 300))
    Mblit(Alpha_screen, warn_text, (800, 450))

    screen.blit(Alpha_screen, (0, 0))
    return player1, player2, tick+1

def n_draw_flop(screen, const, var):
    Round, Match, player1, player2 = const
    tick = var

    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    x1, x2 = 400, 600
    if 0 <= tick < 40:
        _, p2card_y = easing((0, -135), (0, 285), m_quadout, tick, 40)
    else:
        _, p2card_y = 0, 285
    p1card_y = 900 - p2card_y

    if 60 <= tick <= 80:
        common_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
        common_surf.blit(player1.common.img_ci, (0, 0))
        common_surf.set_alpha((tick-60)*255/20)
        common_x, common_y = easing((1400, 450), (1200, 450), m_sineout, tick-60, 20)
    if tick > 80 or tick == -1:
        common_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
        common_surf.blit(player1.common.img_ci, (0, 0))
        common_x, common_y = 1200, 450

    if 0 <= tick <= 80: # mode가 바뀔 때 tick = -1임.
        myrank = NS[30].render(str2Kr(player1.rank2p(player1.showc[-2:])), True, White)
        yourrank = NS[30].render(str2Kr(player2.rank2p(player2.showc[-2:])), True, White)
    else:
        myrank = NS[30].render(str2Kr(player1.rank3p(player1.showc)), True, White)
        yourrank = NS[30].render(str2Kr(player2.rank3p(player2.showc)), True, White)
    coin_text = NS[30].render(str(player1.coin), True, White)

    screen.blit(bg1, (0, 0))
    Mblit(screen, player1.showc[-2].img_ci, (x1, p1card_y))
    Mblit(screen, player1.showc[-1].img_ci, (x2, p1card_y))
    Mblit(screen, player2.showc[-2].img_ci, (x1, p2card_y))
    Mblit(screen, player2.showc[-1].img_ci, (x2, p2card_y))
    Mblit(screen, myrank, (800, 600), 'ML')
    Mblit(screen, yourrank, (800, 300), 'ML')
    Mblit(screen, Coin_icon, (20, 855), 'ML')
    Mblit(screen, coin_text, (80, 855), 'ML')
    if tick >= 60 or tick == -1: Mblit(screen, common_surf, (common_x, common_y))
    if tick > 80 or tick == -1: Mblit(screen, Next_button, (1580, 20), 'TR')

    return tick+1

def n_draw_result(screen, const, var):
    Round, Match, w = const
    player1, player2, tick = var

    if 0 <= tick < 40:
        _, p2card_y = easing((0, -135), (0, 285), m_quadout, tick, 40)
    if tick >= 40 or tick == -1:
        _, p2card_y = 0, 285
    p1card_y = 900 - p2card_y
    common = player1.common

    if tick >= 40 or tick == -1:
        p1rank_text = NS[32].render(str2Kr(player1.rank()), True, White)
        p2rank_text = NS[32].render(str2Kr(player2.rank()), True, White)
    if tick >= 70 or tick == -1:
        if w == 0: win_text = NSE[96].render('DRAW', True, Black)
        if w == 1: win_text = NSE[96].render('YOU WIN!', True, Black)
        if w == 2: win_text = NSE[96].render('YOU LOSE', True, Black)
    coin_text = NS[30].render(str(player1.coin), True, White)

    screen.blit(bg1, (0, 0))
    Mblit(screen, player1.showc[1].img_ci, (400, 615))
    Mblit(screen, player1.showc[2].img_ci, (600, 615))
    Mblit(screen, player2.showc[1].img_ci, (400, 285))
    Mblit(screen, player2.showc[2].img_ci, (600, 285))
    Mblit(screen, player1.showc[3].img_ci, (800, p1card_y))
    Mblit(screen, player1.showc[4].img_ci, (1000, p1card_y))
    Mblit(screen, player2.showc[3].img_ci, (800, p2card_y))
    Mblit(screen, player2.showc[4].img_ci, (1000, p2card_y))
    Mblit(screen, common.img_ci, (1200, 450))
    if tick >= 40 or tick == -1:
        Mblit(screen, p1rank_text, (800, 820))
        Mblit(screen, p2rank_text, (800, 70))
    if tick >= 70 or tick == -1:
        Mblit(screen, win_text, (800, 450))
        Mblit(screen, Next_button, (1580, 20), 'TR')
    Mblit(screen, Coin_icon, (20, 855), 'ML')
    Mblit(screen, coin_text, (80, 855), 'ML')

    return player1, player2, tick+1

def n_draw_exchange_lose(screen, const, var):
    Match, choose, tickf1 = const
    player1, player2 = var

    c1 = len(player1.card_list)
    s2 = len(player2.shown)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    if choose == 0 or choose == 0.5:
        title = NS[72].render("상대에게 줄 카드를 선택하세요", True, White)
    if choose == 1:
        title = NS[72].render("상대에게 뺏어올 카드를 선택하세요", True, White)
    Match_text = NS[24].render(f'Match {Match}', True, White)
    warn_text = NSE[72].render('Choose more card.', True, Black).convert_alpha()
    warn_text.set_alpha(tickf1*255/30)

    screen.blit(bg1, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - 100*c1 + 200*i
        Mblit(screen, card.img_ci, (x, 615))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x - 90, 480, 180, 270), 3, border_radius = 15)
        if choose == 1:
            pg.draw.rect(Alpha_screen, GreyA, (x - 90, 480, 180, 270), border_radius = 15)
    for j in range(s2):
        card = player2.shown[j]
        x = 900 - 100*s2 + 200*j
        Mblit(screen, card.img_ci, (x, 285))
        if card in player2.active_list:
            pg.draw.rect(screen, Red, (x - 90, 150, 180, 270), 3, border_radius = 15)
        if choose == 0:
            pg.draw.rect(Alpha_screen, GreyA, (x - 90, 150, 180, 270), border_radius = 15)
    
    Mblit(screen, title, (800, 80))
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Next_button, (1580, 20), 'TR')
    Mblit(Alpha_screen, warn_text, (800, 450))
    
    screen.blit(Alpha_screen, (0, 0))
    return player1, player2

def n_draw_exchange_draw(screen, const, var):
    Match, tickf1 = const
    player1, player2 = var
    
    c1 = len(player1.card_list)
    s2 = len(player2.shown)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    title = NS[72].render("상대에게 뺏어올 카드를 선택하세요", True, White)
    Match_text = NS[24].render(f'Match {Match}', True, White)
    warn_text = NSE[72].render('Choose more card.', True, Black).convert_alpha()
    warn_text.set_alpha(tickf1*255/30)

    screen.blit(bg1, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - 100*c1 + 200*i
        Mblit(screen, card.img_ci, (x, 615))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x - 90, 480, 180, 270), 3, border_radius = 15)
        pg.draw.rect(Alpha_screen, GreyA, (x - 90, 480, 180, 270), border_radius = 15)
    for j in range(s2):
        card = player2.shown[j]
        x = 900 - 100*s2 + 200*j
        Mblit(screen, card.img_ci, (x, 285))
        if card in player2.active_list:
            pg.draw.rect(screen, Red, (x - 90, 150, 180, 270), 3, border_radius = 15)
    
    Mblit(screen, title, (800, 80))
    Mblit(screen, Match_text, (20, 20), 'TL')
    Mblit(screen, Next_button, (1580, 20), 'TR')
    Mblit(Alpha_screen, warn_text, (800, 450))
    
    screen.blit(Alpha_screen, (0, 0))

    return player1, player2

def n_draw_exchange_delay(screen, const, var):
    player1 = const
    tick    = var
    c1      = len(player1.card_list)

    screen.blit(bg1, (0, 0))
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    title = NS[60].render('Please wait...', True, White)

    Mblit(screen, title, (800, 70))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img, (x, 615))
    for i in range(8):
        x = 800 + 60*math.sin(math.pi * (i + round(tick/5)) / 4)
        y = 450 + 60*math.cos(math.pi * (i + round(tick/5)) / 4)
        c = list(Red) + [55 + i*200 / 8]
        pg.draw.circle(Alpha_screen, c, (x, y), 10)

    screen.blit(Alpha_screen, (0, 0))
    return tick+1

def n_draw_exchange_result(screen, const, var):
    Match, player1, player2, choose = const
    tick = var

    c1 = len(player1.card_list)
    mycard_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
    mycard_surf.blit(player1.ex_card.img_ci, (0, 0))
    mycard_surf.set_alpha((40-tick)*255/30)
    yourcard_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
    yourcard_surf.blit(player2.ex_card.img_ci, (0, 0))
    yourcard_surf.set_alpha((tick-60)*255/30)
    if tick >= 90:
        title = NS[72].render('교환 결과', True, White)

    screen.blit(bg1, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        if card == player1.ex_card or card == player2.ex_card:
            if 0 <= tick < 10:
                Mblit(screen, mycard_surf, (x, 615))
            if 10 <= tick < 40:
                x, y = easing((x, 615), (x, 215), m_sinein, tick-10, 30)
                Mblit(screen, mycard_surf, (x, y))
            if 60 <= tick < 90:
                x, y = easing((x, 215), (x, 615), m_sineout, tick-60, 30)
                Mblit(screen, yourcard_surf, (x, y))
            if tick >= 90 or tick == -1:
                Mblit(screen, yourcard_surf, (x, 615))
            continue
        Mblit(screen, card.img_ci, (x, 615))
    if tick >= 90:
        Mblit(screen, title, (800, 80))
        Mblit(screen, Next_button, (1580, 20), 'TR')

    return tick+1

def n_draw_delay(screen, var):
    tick = var

    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    screen.blit(bg1, (0, 0))
    for i in range(8):
        x = 800 + 60*math.sin(math.pi * (i + round(tick/5)) / 4)
        y = 450 + 60*math.cos(math.pi * (i + round(tick/5)) / 4)
        c = list(Red) + [55 + i*200 / 8]
        pg.draw.circle(Alpha_screen, c, (x, y), 10)

    screen.blit(Alpha_screen, (0, 0))

    return tick+1