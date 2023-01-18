import pygame as pg
from pygame.locals import *
import sys, time
from obj import *
from start import *
from draw import *

WIDTH = 1600
HEIGHT = 900
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("도둑 포커")
clock = pg.time.Clock()

# win: 한 판이 끝나고 두 player 객체의 승패를 판단
# 내가 이겼으면 1, 상대방이 이겼으면 2, 무승부면 0을 return
def win(player1, player2):
    score1 = player1.str2score(player1.rank())
    score2 = player2.str2score(player2.rank())

    if score1 < -100 and 0 < score2 < 100:
        return 2
    if score2 < -100 and 0 < score1 < 100:
        return 1
    if abs(score1) > abs(score2):
        return 1
    if abs(score2) > abs(score1):
        return 2
    if score1 < 0 and score2 > 0:
        return 2
    if score1 > 0 and score2 < 0:
        return 1
    return 0

def main():

    mode = 'main'
    choose = 0
    Match = 0
    Round = 1
    t, w = 0, -1
    common = None
    r1, r2, dd = 'Straight', [], []

    p1 = Player()
    p2 = Player()
    
    # mode 변수에 따라 실행되는 코드가 달라짐
    while True:
        if mode == 'main':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if in_rect(pos, (800 - 150, 640 - 50, 300, 100)):
                        mode = 'chooseRank'
            
            draw_begin(screen)

            clock.tick(60)
            pg.display.update()

        if mode == 'chooseRank':
            pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if in_rect(pos, (550, 200, 200, 120)):
                        r1 = 'Straight'
                    if in_rect(pos, (850, 200, 200, 120)):
                        r1 = 'Flush'
                    if in_rect(pos, (250, 600, 200, 120)):
                        r2 = []
                    if in_rect(pos, (550, 600, 200, 120)):
                        if 1 in r2: r2.remove(1)
                        else: r2.append(1)
                    if in_rect(pos, (850, 600, 200, 120)):
                        if 2 in r2: r2.remove(2)
                        else: r2.append(2)
                    if in_rect(pos, (1150, 600, 200, 120)):
                        if 4 in r2: r2.remove(4)
                        else: r2.append(4)
                    if in_rect(pos, (1300 - 45, 450 - 30, 90, 60)):
                        r2.sort()
                        mode = 'getMatch'
            
            draw_chooserank(screen, (r1, r2, pos))

            clock.tick(60)
            pg.display.update()

        if mode == 'getMatch':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            
            t = draw_getmatch(screen, t)

            if t == 200:
                mode = 'init'

            clock.tick(60)
            pg.display.update()

        if mode == 'init':
            choose = 0
            t, w = 0, -1
            p1, p2, Match = start(Round, (p1, p2, Match))
            mode = 'phase1'
        
        if mode == 'phase1':
            p2 = phase1(p2)
            if 1 in r2 or 2 in r2:
                mode = 'showDD'
            else:
                mode = 'play'

        if mode == 'showDD':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            if t == 0: dd = get_dd(r2, dd)
            if t == 180: mode = 'play'
            
            t = draw_showDD(screen, dd, t)

            clock.tick(60)
            pg.display.update()
        
        if mode == 'play':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    c1 = len(p1.card_list)
                    for i in range(len(p1.card_list)):
                        if p1.card_list[i] in p1.showc:
                            continue
                        x = 900 - c1*100 + i*200
                        if in_rect(pos, (x - 90, 450, 180, 270)):
                            card = p1.card_list[i]
                            if card in p1.active_list:
                                p1.active_list.remove(card)
                            else:
                                p1.active_list.append(card)
                                if len(p1.active_list) > 2:
                                    del p1.active_list[0]
                    if in_rect(pos, (1300 - 90, 750, 90, 60)):
                        if len(p1.active_list) != 2:
                            print("Wrong number of cards")
                            pg.quit()
                            sys.exit()
                        else:
                            if choose == 0:
                                choose = 0.5
                                mode = 'phase2'
                                p1.showc = p1.active_list.copy() # p2는 지금 받으면 안됨
                            if choose == 1:
                                t = 0
                                mode = 'result'
                                p1.showc = [common] + p1.showc + p1.active_list.copy()
                                p1.active_list = [] # 왜 이걸 여기서 초기화 시키지?
                                p2.showc = [common] + p2.showc + p2.active_list.copy()
                                p2.active_list = []

            p1, p2 = draw_play(screen, (Round, Match, choose), (p1, p2))

            if choose == 0.5: choose = 1
            clock.tick(60)
            pg.display.update()

        if mode == 'phase2':

            p2.showc = p2.active_list.copy()
            for card in p1.showc:
                if not card in p1.shown:
                    p1.shown.append(card)
            for card in p2.showc:
                if not card in p2.shown:
                    p2.shown.append(card)

            t = 0
            mode = 'flop'
        
        if mode == 'flop':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if t >= 60 and event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if in_rect(pos, (1300 - 90, 750, 90, 60)):
                        t = 0
                        p1, p2 = phase2((p1, p2))
                        mode = 'play'
            
            t = draw_flop(screen, (Round, Match, p1, p2), t)
            if t == 60:
                common = get_common()
                p1.common = common
                p2.common = common

            clock.tick(60)
            pg.display.update()

        if mode == 'result':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if t >= 60 and in_rect(pos, (1450 - 90, 750, 90, 60)):
                        Round += 1
                        mode = 'init'
                        if Round == 3:
                            Round = 1
                            mode = 'exchange'
                            choose = 0
                            p1.active_list = []
                            p2.active_list = []
                
            if t == 0:
                for card in p1.showc:
                    if not card == common and not card in p1.shown:
                        p1.shown.append(card)
                for card in p2.showc:
                    if not card == common and not card in p2.shown:
                        p2.shown.append(card)

            p1, p2, t = draw_result(screen, (Round, Match, w), (p1, p2, t))
            if t == 60:
                w = win(p1, p2)
            clock.tick(60)
            pg.display.update()
            
        if mode == 'exchange': # 교환 당할 때 mode도 따로 만들어야됨.
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    c1 = len(p1.card_list)
                    s2 = len(p2.shown)
                    if choose == 0:
                        for i in range(c1):
                            x = 900 - c1*100 + i*200
                            if in_rect(pos, (x - 90, 450, 180, 270)):
                                card = p1.card_list[i]
                                if card in p1.active_list:
                                    p1.active_list.remove(card)
                                else:
                                    p1.active_list.append(card)
                                    if len(p1.active_list) > 1:
                                        del p1.active_list[0]
                        if in_rect(pos, (1300 - 90, 750, 90, 60)):
                            if len(p1.active_list) != 1:
                                print("Wrong number of cards")
                                pg.quit()
                                sys.exit()
                            else:
                                choose = 0.5
                    
                    if choose == 1:
                        for i in range(s2):
                            x = x = 900 - s2*100 + i*200
                            if in_rect(pos, (x - 90, 400 - 270, 180, 270)):
                                card = p2.shown[i]
                                if card in p2.active_list:
                                    p2.active_list.remove(card)
                                else:
                                    p2.active_list.append(card)
                                    if len(p2.active_list) > 1:
                                        del p2.active_list[0]

                        if in_rect(pos, (1300 - 90, 750, 90, 60)):
                            if len(p2.active_list) != 1:
                                print("Wrong number of cards")
                                pg.quit()
                                sys.exit()
                            else:
                                mode = 'exchangeR'
                                p1.card_list.remove(p1.active_list[0])
                                p2.card_list.remove(p2.active_list[0])
                                p1.card_list.append(p2.active_list[0])
                                p2.card_list.append(p1.active_list[0])

            p1, p2 = draw_exchange(screen, (Match, choose), (p1, p2))
            
            if choose == 0.5: choose = 1
            clock.tick(60)
            pg.display.update()

        if mode == 'exchangeR':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if in_rect(pos, (1300 - 90, 750, 90, 60)):
                        t = 0
                        mode = 'getMatch'

            t = draw_exchange_result(screen, (Match, p1), t) # 유령 변수

            clock.tick(60)
            pg.display.update()

if __name__ == '__main__':
    main()