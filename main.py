import pygame as pg
from pygame.locals import *
import sys, time
from obj import *
from setting import *
from draw import *
from eventing import *
from spreadsheet import *

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
ori_screen = pg.Surface((1600, 900))
pg.display.set_caption("도둑 포커")
clock = pg.time.Clock()

# win: 한 판이 끝나고 두 player 객체의 승패를 판단
# 내가 이겼으면 1, 상대방이 이겼으면 2, 무승부면 0을 return
def win(player1, player2):
    score1 = player1.str2score(player1.rank())
    score2 = player2.str2score(player2.rank())
    p1b = 'Black' in player1.rank()
    p2b = 'Black' in player2.rank()

    print("CHECKING HANDS")
    print(f"PLAYER 1 : {player1.showc}")
    print(f"PLAYER 2 : {player2.showc}")

    if 400 <= score1 and player2.isdd: return 2
    if 400 <= score2 and player1.isdd: return 1 # 땡잡이가 플러시 이상의 족보를 잡기
    if p1b and 0 < score2 < 100: return 2
    if p2b and 0 < score1 < 100: return 1  # 개패가 검은 족보를 잡기
    if score1 > score2: return 1
    if score2 > score1: return 2 # 족보의 높낮이
    if p1b and p2b: return 0
    if p1b: return 2
    if p2b: return 1 # 동일 족보에서 검은 족보가 짐.
    return 0

def main():

    mode = 'main'
    choose = 0
    Match = 0
    Round = 1
    Phase = 0
    t, w = 0, -1
    tf1, tf2 = 0, 0 # 조건부 작동되는 tick
    common = None
    Rule = ['Straight', []]
    dd = []

    p1 = Player()
    p2 = Player()
    sp = SP_DB()
    WAITING_TIME = 3600

    # mode 변수에 따라 실행되는 코드가 달라짐
    while True:
        if mode == 'main': # 초록색 게임 시작 화면
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mode = mouse_main((mode, p1))
            
            draw_main(ori_screen)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            clock.tick(60)
            pg.display.update()

        if mode == 'choose_key': # "반과 팀을 선택하세요 하는 화면"
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mode = mouse_choose_key(mode)
                    if mode == "get_match":
                        sp = SP_DB(p1.group, p1.team)
                        
                        sp.enroll_player()
                if event.type == KEYDOWN:
                    p1, tf1, tf2 = key_choose_key(event, (p1, tf1, tf2))
            
            tf1, tf2 = draw_choose_key(ori_screen, p1, (tf1, tf2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            
            clock.tick(60)
            pg.display.update()
        '''
        # if mode == 'chooseRank': # choose one 해서 스트레이트 플러쉬 고민하기
        #     pos = pg.mouse.get_pos()
        #     r1, r2 = Rule
        #     for event in pg.event.get():
        #         if event.type == QUIT:
        #             pg.quit()
        #             sys.exit()
        #         if event.type == MOUSEBUTTONDOWN:
        #             if in_rect(pos, (550, 200, 200, 120)):
        #                 r1 = 'Straight'
        #             if in_rect(pos, (850, 200, 200, 120)):
        #                 r1 = 'Flush'
        #             # if in_rect(pos, (250, 600, 200, 120)):
        #             #     r2 = []
        #             # if in_rect(pos, (550, 600, 200, 120)):
        #             #     if 1 in r2: r2.remove(1)
        #             #     else: r2.append(1)
        #             # if in_rect(pos, (850, 600, 200, 120)):
        #             #     if 2 in r2: r2.remove(2)
        #             #     else: r2.append(2)
        #             # if in_rect(pos, (1150, 600, 200, 120)):
        #             #     if 4 in r2: r2.remove(4)
        #             #     else: r2.append(4)
        #             if in_rect(pos, (1300 - 45, 450 - 30, 90, 60)):
        #                 r2.sort()
        #                 Rule = [r1, r2]
        #                 p1.Rule = Rule
        #                 p2.Rule = Rule
        #                 mode = 'get_match'
            
        #     draw_chooserank(ori_screen, (Rule, pos))
        #     screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
        #     Rule = [r1, r2]

        #     clock.tick(60)
        #     pg.display.update()
        '''

        if mode == 'get_match':  # Finding player - 하는 화면
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            
            t = draw_get_match(ori_screen, t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            if t % WAITING_TIME == 0:
                if sp.get_start_permission(Match+1) :
                    if Phase % 2 == 0:
                        Match += 1 
                        p2num = sp.get_opponent(Match) 
                        p2 = Player( p2num, sp.get_hand(p2num) )


                    #Phase = Phase % 2 + 1
                    #print(Phase)
                    mode = 'reset'

            clock.tick(60)
            pg.display.update()   

        if mode == 'reset': # 죽일 수 있는 모드인줄 알았는데, 역시 잘 돌아가는 코드는 건들면 안됨. 이름만 init => reset으로 바꿈.
            choose = 0
            t, w = 0, -1
            #p1, Match = start(Round, (p1, Match)) # 이 부분 대신에 DB에서 끌고 와야 하지
            if Match == 1:
                p1.card_list = sp.get_hand()
            p1.active_list = []
            p1.showc = []
            p1.Rank = ''
            p2.Rank = ''
            p1.isdd = False
            p2.isdd = False
            if Round == 1:
                p1.pre.append([])
                p2.pre.append([])
            #Match += 1
            if 1 in p1.Rule[1] or 2 in p1.Rule[1]:
                mode = 'showDD'
            else:
                mode = 'play_pre' 
        '''
        # if mode == 'showDD':  # 땡잡이를 보여주는 화면 (지금 안씀)
        #     for event in pg.event.get():
        #         if event.type == QUIT:
        #             pg.quit()
        #             sys.exit()

        #     if t == 0:
        #         dd = get_dd(r2, dd)
        #         p1.dd = dd
        #         p2.dd = dd
        #     if t == 180:
        #         t = -1 # draw_showDD를 지나가면서 t가 0이 되도록. 근데 이렇게 짜는거 진짜 별로다
        #         mode = 'play_pre'
            
        #     t = draw_showDD(ori_screen, dd, t)
        #     screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

        #     clock.tick(60)
        #     pg.display.update()
        '''

        if mode == 'play_pre':  # 카드를 펼치는 애니메이션
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()

            
            t = draw_play_pre(ori_screen, (p1, p2), t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if t == 60:
                t = 0
                mode = 'play'

            clock.tick(60)
            pg.display.update()
        
        if mode == 'play':  # 페이즈 진행
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    p1, p2, mode, choose, t, tf1 = mouse_play((p1, p2, mode, choose, t, tf1))
                    if mode == 'flop_pre':
                        Phase = Phase % 2 + 1
                        sp.upload_playing( hand_cards = p1.active_list, match = Match, round = Round, phase = Phase)
                        p1.active_list = []
                        p2.active_list = []
            p1, p2, t = draw_play(ori_screen, (Round, Match, choose, tf1), (p1, p2, t))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            if tf1: tf1 -= 1

            if choose == 0.5: choose = 1
            clock.tick(60)
            pg.display.update()
        
        if mode == 'flop_pre': #여기에 대기시간 화면 필요 -> 페이즈 1 내고 상대 내는거까지 기다리는 시점
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            
            t = draw_delay(ori_screen, t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            if t % WAITING_TIME == 0 :
                if sp.has_conducted(p2.team, Round, Phase):
                    #p2.active_list = sp.get_playing(p2.team, Phase)
                    if Phase == 1:
                        p2.showc = sp.get_playing(p2.team, Phase)
                        mode = 'flop'
                        t = 0
                    else:
                        p2.showc += sp.get_playing(p2.team, Phase)
                        mode = "result"
                        t = 0 
                    print(f"P2.showc :: {p2.showc}")
                    #Phase = Phase % 2 + 1
            clock.tick(60)
            pg.display.update()
            
        if mode == 'flop': # 카드 내는 애니메이션 
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if t >= 80 and event.type == MOUSEBUTTONDOWN:
                    mode, p1, p2, t = mouse_flop((mode, p1, p2, t))
            
            t = draw_flop(ori_screen, (Round, Match, p1, p2), t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if t == 60:
                #common = get_random_card()
                common = sp.get_common(Round)
                # if 1 in Rule[1]:
                #     while dd[0].color == common.color and dd[0].val == common.val:
                #         common = get_random_card() # 커뮤니티 카드와 땡잡이 중복 방지
                p1.common = common
                p2.common = common
                p1.showc = [common] + p1.showc
                p2.showc = [common] + p2.showc

            clock.tick(60)
            pg.display.update()

        if mode == 'result': # 라운드별 결과
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mode, Round, t, choose, p1, p2 = mouse_result((mode, Round, t, choose, p1, p2))
                
            if t == 0:
                p1.set_shown()
                p2.set_shown()
                w = win(p1, p2)
            if t == 70:
                if w == 0: #무승부
                    p1.coin += 5
                    p1.pre[-1].append(0)
                    p2.pre[-1].append(0)
                if w == 1: #승리
                    p1.coin += 10
                    p1.pre[-1].append(1)
                    p2.pre[-1].append(-1)
                if w == 2: #패배
                    p1.pre[-1].append(-1)
                    p2.pre[-1].append(1)
                sp.update_cell('chips', p1.team+1, p1.coin)
                
                sp.clear_phase()
            if mode == 'result': #가끔 씹힐때 있어서 버그처리
                p1, p2, t = draw_result(ori_screen, (Round, Match, w), (p1, p2, t))
                screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
                
                clock.tick(60)
                pg.display.update()
            
        if mode == 'exchange_lose': # 2패시 카드 고르는 단계
            for event in pg.event.get():
                if event.type == QUIT:   
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mode, choose, tf1, p1, p2 = mouse_exchange_lose((mode, choose, tf1, p1, p2))
                    if mode == "exchange_result" : 
                        sp.update_cell('changed_index', p1.team+1, p1.ex_index)
                        sp.update_cell('changed_index', p2.team+1, p2.ex_index)
                        sp.update_cell("phase", p1.team+1, 3, False)
                        sp.update_cell("phase", p2.team+1, 3, False)
            p1, p2 = draw_exchange_lose(ori_screen, (Match, choose, tf1), (p1, p2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if tf1: tf1 -= 1
            
            if choose == 0.5: choose = 1
            clock.tick(60)
            pg.display.update()

        if mode == 'exchange_draw': # 1승 1패시 고르는 단계
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mode, t, tf1, p1, p2 = mouse_exchange_draw((mode, t, tf1, p1, p2))
                    if mode == "exchange_delay":
                        sp.update_cell("changed_index", p2.team+1, p2.ex_index)
                        sp.update_cell("phase", p1.team+1, 3, False)
            p1, p2 = draw_exchange_draw(ori_screen, (Match, tf1), (p1, p2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if tf1: tf1 -= 1

            clock.tick(60)
            pg.display.update()
        
        if mode == 'exchange_delay':  # 승자의 여유(기다림)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            
            t = draw_exchange_delay(ori_screen, p1, t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if t % WAITING_TIME == 0 and sp.has_conducted(p2.team, 2, 3):
                if sum(p1.pre[-1]) > 0 :
                    p1.ex_index = int(sp.get_acell('changed_index', p1.team+1))
                    p2.ex_index = int(sp.get_acell('changed_index', p2.team+1))
                    p1.ex_card = p1.card_list[p1.ex_index]
                    p2.ex_card = p2.card_list[p2.ex_index]
                    choose = 0
                    t = 0
                    mode = 'exchange_result'
                if sum(p1.pre[-1]) == 0:
                
                    p1.ex_index = int(sp.get_acell('changed_index', p1.team+1))
                    p1.ex_card = p1.card_list[p1.ex_index]
                    
                    choose = 0
                    t = 0
                    mode = 'exchange_result'
            clock.tick(60)
            pg.display.update()

        if mode == 'exchange_result': #교환 후 결과 보여주는 화면
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if t >= 90 and event.type == MOUSEBUTTONDOWN:
                    mode, t = mouse_exchange_result((mode, t))

                    if mode == "get_match":
                        sp.upload_hand(hand_cards = p1.card_list)


            if t == 50:
                p1.card_list[p1.ex_index] = p2.ex_card
                p2.card_list[p2.ex_index] = p1.ex_card
            
            t = draw_exchange_result(ori_screen, (Match, p1, p2, choose), t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            clock.tick(60)
            pg.display.update()

        if mode == 'delay': # 대기 화면 (DB에서 갖고오는 동안 등) (아직 사용하고 있지는 않음)
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
            
            t = draw_delay(ori_screen, t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            clock.tick(60)
            pg.display.update()

if __name__ == '__main__':
    main()