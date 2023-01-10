import pygame as pg
from pygame.locals import *
import sys, time, os
from obj import *
from start import *
from draw import *

pg.init()
screen = pg.display.set_mode((1200, 900))
pg.display.set_caption("도둑 포커")
clock = pg.time.Clock()

def in_rect(pos, rect):
    return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]

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
        return 1
    if score1 > 0 and score2 < 0:
        return 2
    return 0

def main():

    mode = 'init'
    choose = 0
    Round = 1
    t, w = 0, -1

    p1 = Player()
    p2 = Player()

    while True:
        if mode == 'init':
            choose = 0
            t, w = 0, -1
            p1, p2 = start(Round, (p1, p2))
            mode = 'phase1'
        
        if mode == 'phase1':
            p1, p2 = phase1(Round, (p1, p2))
            mode = 'play'
        
        if mode == 'play':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    if choose == 0:
                        for i in range(len(p1.card_list)):
                            if in_rect(pos, (10 + i*200, 450, 180, 270)): # 6장 기준
                                card = p1.card_list[i]
                                if card in p1.active_list:
                                    p1.active_list.remove(card)
                                else:
                                    p1.active_list.append(card)
                        if in_rect(pos, (800, 750, 90, 60)):
                            if len(p1.active_list) != 2:
                                print("Wrong number of cards")
                                pg.quit()
                                sys.exit()
                            else:
                                mode = 'phase2'
                                choose = 0.5
                                p1.showc = p1.active_list.copy()

                    if choose == 1:
                        for i in range(6):
                            if p1.card_list[i] in p1.showc:
                                continue
                            if in_rect(pos, (10 + i*200, 450, 180, 270)):
                                card = p1.card_list[i]
                                if card in p1.active_list:
                                    p1.active_list.remove(card)
                                else:
                                    p1.active_list.append(card)
                        if in_rect(pos, (800, 750, 90, 60)):
                            if len(p1.active_list) != 2:
                                print("Wrong number of cards")
                                pg.quit()
                                sys.exit()
                            else:
                                mode = 'result'
                                choose = 2
                                p1.showc = p1.showc + p1.active_list.copy()
                                p1.active_list = []
                                p2.showc = p2.showc + p2.active_list.copy()
                                p2.active_list = []

            
            p1, p2 = draw_play(screen, (Round, choose), (p1, p2))
            if choose == 0.5:
                choose = 1

            clock.tick(60)
            pg.display.update()

        if mode == 'phase2':
            draw_flop(screen, (p1, p2))
            pg.display.update()
            time.sleep(2)

            p1, p2 = phase2(Round, (p1, p2))
            mode = 'play'

        if mode == 'result':
            p1, p2, t = draw_result(screen, w, (p1, p2, t))
            if t == 60:
                w = win(p1, p2)
            if t == 240:
                t = 0
                Round += 1
                mode = 'init'
                if Round == 3:
                    mode = 'exchange'
                    choose = 0
                    p1.active_list = []
                    p2.active_list = []
            clock.tick(60)
            pg.display.update()
            
        if mode == 'exchange': # 교환 당할 때 mode도 따로 만들어야됨.
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()

                    if choose == 0:
                        for i in range(6):
                            if in_rect(pos, (10 + i*200, 450, 180, 270)):
                                card = p1.card_list[i]
                                if card in p1.active_list:
                                    p1.active_list.remove(card)
                                else:
                                    p1.active_list.append(card)
                        if in_rect(pos, (800, 750, 90, 60)):
                            if len(p1.active_list) != 1:
                                print("Wrong number of cards")
                                pg.quit()
                                sys.exit()
                            else:
                                choose = 0.5
                    
                    if choose == 1:
                        for i in range(len(p2.showc)):
                            if in_rect(pos, (610 - 100 * len(p2.shown)+ i*200, 150, 180, 270)):
                                card = p2.shown[i]
                                if card in p2.active_list:
                                    p2.active_list.remove(card)
                                else:
                                    p2.active_list.append(card)
                        if in_rect(pos, (800, 750, 90, 60)):
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

            p1, p2 = draw_exchange(screen, choose, (p1, p2))
            
            if choose == 0.5: choose = 1
            clock.tick(60)
            pg.display.update()

        if mode == 'exchangeR':
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            t = draw_exchange_result(screen, p1, t)
            if t == 240:
                pg.quit()
                sys.exit()

            clock.tick(60)
            pg.display.update()

if __name__ == '__main__':
    main()