import pygame as pg
from pygame.locals import *
from obj import *
from moving import *
import math
pg.init()

bg_list = []
for i in range(5):
    bg_list.append(pg.transform.scale(pg.image.load(resource_path(img_dir_path + f'com_bg_{i+1}.png')), (1600, 900)))
bg1, bg2, bg3, bg4, bg5 = bg_list

def Mblit(screen, surf, pos, poscon = 'MM', rel_pos = True):
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

def Mrect(screen, color, rect, width = 0, rectcon = 'MM', border_radius = 0):
    x, y, w, h = rect
    r, c = rectcon
    if r == 'T': y = y
    elif r == 'M': y = y - h/2
    elif r == 'B': y = y - h
    else: raise NameError('Wrong condition')
    if   c == 'L': x = x
    elif c == 'M': x = x - w/2
    elif c == 'R': x = x - w
    else: raise NameError('Wrong condition')

    pg.draw.rect(screen, color, (x, y, w, h), width, border_radius = border_radius)

def str2Kr(s):
    col_kr_dict = {'Red': '빨강', 'Blue': '파랑', 'Yellow': '노랑', 'Green': '초록'}
    blacks = '검은' if 'Black' in s else ''
    if 'Straight-Flush' in s:
        i = s.find(' ', s.find(' ')+1)
        return f'{blacks} {col_kr_dict[s[2:i]]} {s[0]} 스티플'
    if 'Four of a kind' in s:
        return f'{blacks} {s[0]} 포카드'
    if 'Straight' in s:
        return f'{blacks} {s[0]} 스트레이트'
    if 'Flush' in s:
        i = s.find(' ')
        j = s.find('(')
        return f'{blacks} {col_kr_dict[s[:i]]} 플러시 {s[j:]}'
    if 'Three of a kind' in s:
        return f'{blacks} {s[0]} 트리플'
    if 'Two pair' in s:
        return f'{blacks} {s[:3]} 투 페어'
    if 'Pair' in s:
        return f'{blacks} {s[0]} 원 페어'
    return f'노 페어 {s[8:]}'

NS  = [pg.font.Font(resource_path(img_dir_path + '/BMJUA_otf.otf'), x) for x in range(1, 100)]
NSE = [pg.font.Font(resource_path(img_dir_path + '/a가을운동회M.ttf'), x) for x in range(1, 100)]
NS.insert(0, 0)
NSE.insert(0, 0)

Next_button = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Next_button.png')), (90, 60))
Rank_button = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Rank_button.png')), (90, 60))
Coin_icon = pg.transform.scale((pg.image.load(resource_path(img_dir_path + 'coin.png'))), (50, 50))
Jokbo_button = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Jokbo_button.png')), (90, 60))
white_bg = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'white_bg.png')), (1600, 900))
white_bg.set_alpha(128)
Jokbo_ver1 = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Jokbo_ver1.png')), (500, 888))
Jokbo_ver2 = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Jokbo_ver2.png')), (500, 888))
Jokbo_ver3 = pg.transform.scale(pg.image.load(resource_path(img_dir_path + 'Jokbo_ver3.png')), (500, 888))

def draw_option(screen, csize, cqsize):

    option_text = NS[36].render('Option', True, White)
    size_text = NS[30].render('화면 크기', True, White)
    Alpha_screen = pg.Surface((400, 700), pg.SRCALPHA)
    
    wid = csize[0]
    color_list = list(map(lambda b: Red if b else White, [wid == 1920, wid == 1600, wid == 1440, wid == 1280]))
    XL_screen_text     = NSE[36].render('1920 X 1080', True, color_list[0])
    large_screen_text  = NSE[36].render('1600 X 900', True, color_list[1])
    medium_screen_text = NSE[36].render('1440 X 810', True, color_list[2])
    small_screen_text  = NSE[36].render('1280 X 720', True, color_list[3])

    qwid = cqsize[0]
    color_list = list(map(lambda b: Red if b else White, [qwid == 1920, qwid == 1600, qwid == 1440, qwid == 1280]))
    quality_text = NS[30].render('품질', True, White)
    best_quality_text   = NS[36].render('최상', True, color_list[0])
    high_quality_text   = NS[36].render('좋음', True, color_list[1])
    medium_quality_text = NS[36].render('보통', True, color_list[2])
    low_quality_text    = NS[36].render('구림', True, color_list[3])
    apply_text = NS[30].render('확인', True, Black)

    Alpha_screen.fill(GreyB)
    Mblit(Alpha_screen, option_text, (200, 50))
    Mblit(Alpha_screen, size_text, (20, 110), 'ML')
    pg.draw.rect(Alpha_screen, GreyC, (20, 140, 360, 60))
    pg.draw.rect(Alpha_screen, GreyC, (20, 210, 360, 60))
    pg.draw.rect(Alpha_screen, GreyC, (20, 280, 360, 60))
    pg.draw.rect(Alpha_screen, GreyC, (20, 350, 360, 60))
    Mblit(Alpha_screen, XL_screen_text,     (200, 170))
    Mblit(Alpha_screen, large_screen_text,  (200, 240))
    Mblit(Alpha_screen, medium_screen_text, (200, 310))
    Mblit(Alpha_screen, small_screen_text,  (200, 380))
    
    Mblit(Alpha_screen, quality_text, (20, 450), 'ML')
    pg.draw.rect(Alpha_screen, GreyC, (5, 480, 90, 90))
    pg.draw.rect(Alpha_screen, GreyC, (105, 480, 90, 90))
    pg.draw.rect(Alpha_screen, GreyC, (205, 480, 90, 90))
    pg.draw.rect(Alpha_screen, GreyC, (305, 480, 90, 90))
    Mblit(Alpha_screen, low_quality_text,    (50, 525))
    Mblit(Alpha_screen, medium_quality_text, (150, 525))
    Mblit(Alpha_screen, high_quality_text,   (250, 525))
    Mblit(Alpha_screen, best_quality_text,   (350, 525))

    pg.draw.rect(Alpha_screen, list(Pink)+[235], (380-90, 680-60, 90, 60))
    Mblit(Alpha_screen, apply_text, (335, 650))
    Mblit(screen, Alpha_screen, (800, 450))
    

def draw_main(screen):
    title = NSE[96].render("도둑  포커", True, White)
    single_text = NS[50].render("싱글 모드", True, Black)
    multi_text  = NS[50].render("멀티 모드", True, Black)
    resume_text = NS[50].render("재접속 모드", True, Black)
    
    screen.blit(bg3, (0, 0))
    Mblit(screen, title, (800, 250))
    pg.draw.rect(screen, Brown1, (320, 600, 300, 100))
    pg.draw.rect(screen, Brown1, (650, 600, 300, 100))
    pg.draw.rect(screen, Brown1, (980, 600, 300, 100))
    Mblit(screen, single_text, (470, 650))
    Mblit(screen, multi_text, (800, 650))
    Mblit(screen, resume_text, (1130, 650))
    
def draw_choose_key(screen, const, var):
    p1 = const
    tickf1, tickf2 = var

    class_val = p1.group
    team_val  = p1.team

    title = NS[80].render("반과  팀을  선택하세요", True, Black)
    subtitle = NS[48].render("방향키로 작동합니다", True, Black)
    class_text = NS[48].render("반", True, Black)
    team_text = NS[48].render("팀", True, Black)
    class_val_text = NSE[72].render(str(class_val), True, (8*tickf1, 26/30*tickf1, 0))
    team_val_text = NSE[72].render(str(team_val), True,   (8*tickf2, 26/30*tickf2, 0))

    screen.fill(Grey1)
    Mblit(screen, title, (800, 100))
    Mblit(screen, subtitle, (800, 190))
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

def draw_get_match(screen, const, var):
    player1, hover, text_index, Match = const
    tick = var

    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    title = NS[72].render("게임 준비 중...", True, Black)
    dyk_text = NS[28].render("알고 계셨나요?", True, Black)
    mozaic_text = NS[28].render("1g(3#$%%b72q@!@TY#N$\\3tmt18:ns;riu7tv", True, Black)
    dyk_text = pg.transform.rotate(dyk_text, 10)
    if len(Didyouknow[text_index]) == 1:
        TMI_text_1 = NS[35].render(Didyouknow[text_index][0], True, Grey3)
    if len(Didyouknow[text_index]) == 2:
        TMI_text_1 = NS[31].render(Didyouknow[text_index][0], True, Grey3)
        TMI_text_2 = NS[31].render(Didyouknow[text_index][1], True, Grey3)
    if not hover == -1: desc_text = NS[30].render(Item_desc[hover], True, Black)
    group_text  = NS[40].render(f'Group {player1.group}', True, Black)
    myteam_text = NS[40].render(f'Team {player1.team}',  True, Black)
    j = 0

    screen.fill(Grey1)
    Mblit(screen, title, (800, 100))
    if not Match == 7:
        Mblit(screen, dyk_text, (300, 135))
        if len(Didyouknow[text_index]) == 1:
            Mblit(screen, TMI_text_1, (800, 200))
        if len(Didyouknow[text_index]) == 2:
            Mblit(screen, TMI_text_1, (800, 180))
            Mblit(screen, TMI_text_2, (800, 220))
    if Match == 7:
        Mblit(screen, mozaic_text, (300, 135))
    for i in range(5):
        num_text = NS[18].render(str(player1.item[i]), True, Black)
        if player1.item[i]:
            Mblit(screen, Item_IMGlist[i], (100 + 200*j, 750))
            Mblit(screen, num_text, (170 + 200*j, 860))
            if player1.using_item == i: Mrect(screen, Red, (100 + 200*j, 750, 160, 240), 3)
            j += 1
    if not hover == -1: Mblit(screen, desc_text, (800, 590))

    Mblit(screen, group_text, (1280, 830), 'BR')
    Mblit(screen, myteam_text, (1280, 880), 'BR')
    screen.blit(Alpha_screen, (0, 0))
    return tick+1

def draw_play_pre(screen, const, var):
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

def draw_play(screen, const, var):
    Round, Match, choose, tickf1, (item_x1, item_x2) = const
    player1, player2, tick = var

    c1 = len(player1.card_list)
    c2 = len(player2.card_list)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)

    match_text = NSE[36].render(str(Match), True, White)
    round_text = NSE[36].render(str(Round), True, White)
    myteam_text = NS[40].render(f'Team {player1.team}', True, White)
    yourteam_text = NSE[48].render(str(player2.team), True, Black)
    warn_text = NS[72].render('Choose more card.', True, Black).convert_alpha()
    warn_text.set_alpha(tickf1*255/30)
    coin_text = NSE[36].render(str(player1.coin), True, White)
    common_card = player1.common

    p2_isblack = False
    for card in player2.card_list:
        if card.color == 'Black':
            p2_isblack = True
    if p2_isblack or player1.using_item == 2:
        blackcard_text = NSE[24].render("! 조커 있음 !", True, Pink)
        peeping_text = NSE[24].render("엿보기 중", True, Blue)
        if tick % 60 < 30:
            _, flowing_y = easing((800, 180), (800, 160), m_sineinout, tick%60, 30)
        else:
            _, flowing_y = easing((800, 160), (800, 180), m_sineinout, tick%60 - 30, 30)


    screen.blit(bg2, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x, y = 850 - c1*50 + 100*i, 700
        Mblit(screen, card.img_half, (x, y))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x-150, y-225, 300, 450), 4, border_radius = 30)
        if choose == 1 and card in player1.showc:
            pg.draw.rect(screen, Grey3, (x-150, y-225, 300, 450), 10, border_radius = 30)
        if player1.using_item == 1 and (i == item_x1 or i == item_x2):
            if tick % 60 < 30:
                ix, iy = easing((x-80, y-260), (x-80, y-250), m_sineinout, tick%60, 30)
            else:
                ix, iy = easing((x-80, y-250), (x-80, y-260), m_sineinout, tick%60 - 30, 30)
            Mblit(screen, arrow_img, (ix, iy))
    
    if choose == 0 or choose == 0.5:
        for i in range(c2):
            card = player2.card_list[i]
            x, y = 820 - c2*20 + i*40, 300
            if player1.using_item == 2 and (item_x1 == i or item_x2 == i):
                Mblit(screen, Card.shrink(card.img, 1/5), (x, y))
                peep_surf = pg.Surface((120, 180), pg.SRCALPHA)
                pg.draw.rect(peep_surf, list(Blue)+[127], (0, 0, 120, 180), border_radius = 8)
                Mblit(screen, peep_surf, (x, y))
            else: Mblit(screen, Card.shrink(Card_IMGlist['Hide'], 1/5), (x, y))
    if choose == 1:
        j = 0
        Mblit(screen, Card.shrink(player2.showc[-2].img, 1/5), (350, 300))
        Mblit(screen, Card.shrink(player2.showc[-1].img, 1/5), (480, 300))
        for i in range(c2):
            card = player2.card_list[i]
            if card in player2.showc: continue
            x, y = 820 - (c2-2)*20 + j*40, 300
            if player1.using_item == 2 and (item_x1 == i or item_x2 == i):
                Mblit(screen, Card.shrink(card.img, 1/5), (x, y))
                peep_surf = pg.Surface((120, 180), pg.SRCALPHA)
                pg.draw.rect(peep_surf, list(Blue)+[127], (0, 0, 120, 180), border_radius = 8)
                Mblit(screen, peep_surf, (x, y))
            else: Mblit(screen, Card.shrink(Card_IMGlist['Hide'], 1/5), (x, y))
            j += 1
        Mblit(screen, common_card.img_std, (1300, 300))
        pg.draw.rect(screen, Yellow, (1195, 150, 210, 300), 3, border_radius = 15)

    pg.draw.circle(screen, White, (180, 450), 50)
    Mblit(screen, match_text, (180, 43), 'ML')
    Mblit(screen, round_text, (180, 91), 'ML')
    Mblit(screen, coin_text, (180, 139), 'ML')
    Mblit(screen, Next_button, (1580, 880), 'BR')
    Mblit(screen, Jokbo_button, (1580, 90), 'TR')
    Mblit(screen, myteam_text, (1580, 20), 'TR')
    Mblit(screen, yourteam_text, (180, 450))
    Mblit(Alpha_screen, warn_text, (800, 450))
    if p2_isblack: Mblit(screen, blackcard_text, (800, flowing_y))
    if player1.using_item == 2: Mblit(screen, peeping_text, (800, flowing_y - 30))

    screen.blit(Alpha_screen, (0, 0))
    
    return player1, player2, tick+1

def draw_play_delay(screen, const, var):
    player1, player2, phase = const
    tick = var

    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    c1 = len(player1.card_list)
    x0 = 850 - c1*50

    screen.blit(bg5, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        Mblit(screen, card.img_half, (x0 + i*100, 700))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x0 + i*100 - 150, 475, 300, 450), 4, border_radius = 30)
        if phase == 2 and card in player1.showc and not card in player1.active_list:
            pg.draw.rect(screen, Grey3, (x0 + i*100 - 150, 475, 300, 450), 10, border_radius = 30)
    for i in range(8):
        x = 800 + 60*math.sin(math.pi * (i + round(tick/5)) / 4)
        y = 450 + 60*math.cos(math.pi * (i + round(tick/5)) / 4)
        c = list(Red) + [55 + i*200 / 8]
        pg.draw.circle(Alpha_screen, c, (x, y), 10)

    screen.blit(Alpha_screen, (0, 0))
    return tick+1

def draw_flop(screen, const, var):
    Round, Match, player1, player2 = const
    tick = var

    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    mx1, mx2 = 327, 607
    yx1, yx2 = 387, 627
    if 0 <= tick < 40:
        _, p1card_y = easing((0, 900), (0, 547), m_quadout, tick, 40)
        _, p2card_y = easing((0, 0), (0, 218), m_quadout, tick, 40)
    else:
        _, p1card_y = 0, 547
        _, p2card_y = 0, 218

    if 60 <= tick <= 80:
        common_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
        common_surf.blit(player1.common.img_std, (0, 0))
        common_surf.set_alpha((tick-60)*255/20)
        common_x, common_y = easing((1727, 383), (1427, 383), m_sineout, tick-60, 20)
    if tick > 80 or tick == -1:
        common_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
        common_surf.blit(player1.common.img_std, (0, 0))
        common_x, common_y = 1427, 383
    myteam_text = NS[40].render(f'Team {player1.team}', True, White)

    if 0 <= tick <= 80: # mode가 바뀔 때 tick = -1임.
        p1rank_text = NS[40].render(str2Kr(player1.rank2p(player1.showc[-2:])), True, White)
        p2rank_text = NS[38].render(str2Kr(player2.rank2p(player2.showc[-2:])), True, White)
    else:
        p1rank_text = NS[40].render(str2Kr(player1.rank3p(player1.showc)), True, White)
        p2rank_text = NS[38].render(str2Kr(player2.rank3p(player2.showc)), True, White)

    screen.blit(bg1, (0, 0))
    Mblit(screen, player1.showc[-2].img_std, (mx1, p1card_y))
    Mblit(screen, player1.showc[-1].img_std, (mx2, p1card_y))
    Mblit(screen, player2.showc[-2].img_small, (yx1, p2card_y))
    Mblit(screen, player2.showc[-1].img_small, (yx2, p2card_y))
    Mblit(screen, p1rank_text, (800, 740))
    Mblit(screen, p2rank_text, (800, 50))
    Mblit(screen, myteam_text, (1580, 20), 'TR')
    if tick >= 60 or tick == -1: Mblit(screen, common_surf, (common_x, common_y))
    if tick > 80 or tick == -1: Mblit(screen, Next_button, (1580, 880), 'BR')

    return tick+1

def draw_result(screen, const, var):
    Round, Match, w = const
    player1, player2, tick = var

    if 0 <= tick < 40:
        _, p1card_y = easing((0, 900), (0, 547), m_quadout, tick, 40)
        _, p2card_y = easing((0, 0), (0, 218), m_quadout, tick, 40)
    if tick >= 40 or tick == -1:
        _, p1card_y = 0, 547
        _, p2card_y = 0, 218
    common = player1.common

    if tick >= 40 or tick == -1:
        score1 = player1.str2score(player1.rank())
        score2 = player2.str2score(player2.rank())
        if 400 <= score1 < 600 and player2.isdd: p2rank_text = NS[38].render('레인보우', True, White)
        else: p2rank_text = NS[38].render(str2Kr(player2.rank()), True, White)
        if 400 <= score2 < 600 and player1.isdd: p1rank_text = NS[40].render('레인보우', True, White)
        else: p1rank_text = NS[40].render(str2Kr(player1.rank()), True, White)
    if tick >= 70 or tick == -1:
        if w == 0: win_text = NSE[96].render('DRAW',     True, Blue2)
        if w == 1: win_text = NSE[96].render('YOU WIN!', True, Blue2)
        if w == 2: win_text = NSE[96].render('YOU LOSE', True, Blue2)
    coin_text = NS[30].render(str(player1.coin), True, White)
    myteam_text = NS[40].render(f'Team {player1.team}', True, White)

    screen.blit(bg1, (0, 0))
    Mblit(screen, player1.showc[1].img_std,   (327, 547))
    Mblit(screen, player1.showc[2].img_std,   (607, 547))
    Mblit(screen, player2.showc[1].img_small, (387, 218))
    Mblit(screen, player2.showc[2].img_small, (627, 218))
    Mblit(screen, player1.showc[3].img_std,   (887, p1card_y))
    Mblit(screen, player1.showc[4].img_std,   (1167, p1card_y))
    Mblit(screen, player2.showc[3].img_small, (867, p2card_y))
    Mblit(screen, player2.showc[4].img_small, (1107, p2card_y))
    Mblit(screen, common.img_std, (1427, 383))
    if tick >= 40 or tick == -1:
        Mblit(screen, p1rank_text, (800, 740))
        Mblit(screen, p2rank_text, (800, 50))
    if tick >= 70 or tick == -1:
        Mblit(screen, win_text, (800, 400))
        Mblit(screen, Next_button, (1580, 880), 'BR')
    Mblit(screen, Coin_icon, (20, 855), 'ML')
    Mblit(screen, coin_text, (80, 855), 'ML')
    Mblit(screen, myteam_text, (1580, 20), 'TR')

    return player1, player2, tick+1

def draw_exchange_lose(screen, const, var):
    Match, choose, tickf1 = const
    player1, player2 = var

    c1 = len(player1.card_list)
    s2 = len(player2.shown)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    if choose == 0 or choose == 0.5:
        title = NS[72].render("상대에게 줄 카드를 선택하세요", True, White)
    if choose == 1:
        title = NS[72].render("상대에게 뺏어올 카드를 선택하세요", True, White)
    warn_text = NS[72].render('Choose more card.', True, Black).convert_alpha()
    warn_text.set_alpha(tickf1*255/30)
    myteam_text = NS[40].render(f'Team {player1.team}', True, White)

    screen.blit(bg4, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - 100*c1 + 200*i
        Mblit(screen, card.img_std, (x, 615))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x - 90, 480, 180, 270), 3, border_radius = 15)
        if choose == 1:
            pg.draw.rect(Alpha_screen, GreyA, (x - 90, 480, 180, 270), border_radius = 15)
    for j in range(s2):
        card = player2.shown[j]
        x = 900 - 100*s2 + 200*j
        Mblit(screen, card.img_std, (x, 285))
        if card in player2.active_list:
            pg.draw.rect(screen, Red, (x - 90, 150, 180, 270), 3, border_radius = 15)
        if choose == 0:
            pg.draw.rect(Alpha_screen, GreyA, (x - 90, 150, 180, 270), border_radius = 15)
    
    Mblit(screen, title, (800, 80))
    Mblit(screen, myteam_text, (1580, 20), 'TR')
    Mblit(screen, Next_button, (1580, 880), 'BR')
    Mblit(Alpha_screen, warn_text, (800, 450))
    
    screen.blit(Alpha_screen, (0, 0))
    return player1, player2

def draw_exchange_draw(screen, const, var):
    Match, tickf1 = const
    player1, player2 = var
    
    c1 = len(player1.card_list)
    s2 = len(player2.shown)
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    title = NS[72].render("상대에게 뺏어올 카드를 선택하세요", True, White)
    warn_text = NS[72].render('Choose more card.', True, Black).convert_alpha()
    warn_text.set_alpha(tickf1*255/30)
    myteam_text = NS[40].render(f'Team {player1.team}', True, White)

    screen.blit(bg4, (0, 0))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - 100*c1 + 200*i
        Mblit(screen, card.img_std, (x, 615))
        if card in player1.active_list:
            pg.draw.rect(screen, Red, (x - 90, 480, 180, 270), 3, border_radius = 15)
        pg.draw.rect(Alpha_screen, GreyA, (x - 90, 480, 180, 270), border_radius = 15)
    for j in range(s2):
        card = player2.shown[j]
        x = 900 - 100*s2 + 200*j
        Mblit(screen, card.img_std, (x, 285))
        if card in player2.active_list:
            pg.draw.rect(screen, Red, (x - 90, 150, 180, 270), 3, border_radius = 15)
    
    Mblit(screen, title, (800, 80))
    Mblit(screen, myteam_text, (1580, 20), 'TR')
    Mblit(screen, Next_button, (1580, 880), 'BR')
    Mblit(Alpha_screen, warn_text, (800, 450))
    
    screen.blit(Alpha_screen, (0, 0))

    return player1, player2

def draw_exchange_delay(screen, const, var):
    player1 = const
    tick    = var
    c1      = len(player1.card_list)

    screen.blit(bg4, (0, 0))
    Alpha_screen = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
    title = NS[60].render('교환 중...', True, White)

    Mblit(screen, title, (800, 70))
    for i in range(c1):
        card = player1.card_list[i]
        x = 900 - c1*100 + i*200
        Mblit(screen, card.img_std, (x, 615))
    for i in range(8):
        x = 800 + 60*math.sin(math.pi * (i + round(tick/5)) / 4)
        y = 450 + 60*math.cos(math.pi * (i + round(tick/5)) / 4)
        c = list(Red) + [55 + i*200 / 8]
        pg.draw.circle(Alpha_screen, c, (x, y), 10)

    screen.blit(Alpha_screen, (0, 0))
    return tick+1

def draw_exchange_result(screen, const, var):
    Match, player1, player2, choose = const
    tick = var

    c1 = len(player1.card_list)
    mycard_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
    mycard_surf.blit(player1.ex_card.img_std, (0, 0))
    mycard_surf.set_alpha((40-tick)*255/30)
    yourcard_surf = pg.Surface((180, 270), pg.SRCALPHA).convert_alpha()
    yourcard_surf.blit(player2.ex_card.img_std, (0, 0))
    yourcard_surf.set_alpha((tick-60)*255/30)
    if tick >= 90:
        title = NS[72].render('교환  결과', True, White)
    myteam_text = NS[40].render(f'Team {player1.team}', True, White)

    screen.blit(bg4, (0, 0))
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
        Mblit(screen, card.img_std, (x, 615))
    Mblit(screen, myteam_text, (1580, 20), 'TR')
    if tick >= 90:
        Mblit(screen, title, (800, 80))
        Mblit(screen, Next_button, (1580, 880), 'BR')

    return tick+1

def draw_delay(screen, var):
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

def draw_end(screen, var):
    player1, coin, tickf1, tickf2, tick = var

    title = NSE[96].render('Game End!', True, Black)
    coin_text = NS[36].render('보유 코인: ', True, Black)
    coin_amoumt_text = NSE[96].render(str(coin), True, (3.5*tickf1, 3*tickf1, 0))
    item0_img = Item_IMGlist[0].convert_alpha()
    item0_img.set_alpha(tickf2*255/30)

    screen.fill(Grey1)
    Mblit(screen, title, (800, 150))
    Mblit(screen, coin_text, (700, 450))
    Mblit(screen, coin_amoumt_text, (900, 450))
    for i, card in enumerate(player1.card_list):
        if tick < 50*i : x, y = -200, 750
        if 50*i <= tick < 50 + 50*i: x, y = easing((-200, 750), (800, 750), m_quadout, tick-50*i, 50)
        if 50 + 50*i <= tick <= 100 + 50*i: x, y = easing((800, 750), (1800, 750), m_quadin, tick-50*(i+1), 50)
        if tick > 100 + 50*i: x, y = 1800, 750
        Mblit(screen, card.img_std, (x, y))

        if tick == 50 + 50*i and card.color == 'Black':
            if player1.item[0] == 0: coin = int(coin * 0.8)
            else:
                player1.item[0] -= 1
                coin = int(coin * 0.95)
                tickf2 = 30
            tickf1 = 60
    if tickf1: tickf1 -= 1
    if tickf2:
        Mblit(screen, item0_img, (1200, 450))
        tickf2 -= 1

    return player1, coin, tickf1, tickf2, tick+1

def draw_credit(screen):
    title = NSE[72].render("도둑 포커", True, Black)
    developer_text = NSE[60].render("프로그램 개발자: 임찬열, 권혁원", True, Black)
    myteam_text    = NSE[36].render("도둑포커 팀: 배서위, 박정원, 임선재, 정재원, 전재민, 차민, 탁건우", True, Black)
    joojup1_text   = NSE[48].render("도둑 포커는 서비스 종료입니다ㅠㅠ", True, Black)
    joojup2_text   = NSE[48].render("혹시 게임이 다시 하고 싶다면 개발자에게 메일로 연락해주세용^^", True, Black)

    screen.fill(Grey1)
    Mblit(screen, title, (800, 100))
    Mblit(screen, developer_text, (800, 300))
    Mblit(screen, myteam_text,    (800, 370))
    Mblit(screen, joojup1_text,   (800, 500))
    Mblit(screen, joojup2_text,   (800, 550))

def draw_jokbo(screen, Match):
    Mblit(screen, white_bg, (800, 450))
    if Match >= 1 and Match <= 3:
        Mblit(screen, Jokbo_ver1, (800, 450))
    elif Match <= 7:
        Mblit(screen, Jokbo_ver2, (800, 450))
    elif Match <= 14:
        Mblit(screen, Jokbo_ver3, (800, 450))        

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")