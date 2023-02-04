import pygame as pg
from pygame.locals import *
import sys, time, random
from obj import *
from setting import *
from draw import *
from eventing import *
from spreadsheet import *

pg.init()
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

    if 400 <= score1 < 600 and player2.isdd: return 2
    if 400 <= score2 < 600 and player1.isdd: return 1 # 땡잡이가 플러시 이상의 족보를 잡기
    if p1b and 0 < score2 < 100: return 2
    if p2b and 0 < score1 < 100: return 1  # 개패가 검은 족보를 잡기
    if score1 // 100 > score2 // 100: return 1
    if score2 // 100 > score1 // 100: return 2 # 족보의 높낮이 (큰 차이)
    if p1b and not p2b: return 2
    if p2b and not p1b: return 1 # 비슷한 족보에서 검은 족보가 짐.
    if score1 > score2: return 1
    if score2 > score1: return 2 # 비슷한 족보에서 세부 족보
    return 0

def set_para(Match):
    if 1 <= Match <= 3: v = 0
    if 4 <= Match <= 7: v = 1
    if 8 <= Match <= 10: v = 2
    if 11 <= Match <= 14: v = 3
    Rule = MATCH_PARA[v][:2]
    reward_coin = MATCH_PARA[v][2]

    return Rule[0], Rule[1], reward_coin

def main():

    WIDTH, HEIGHT = 1600, 900
    QWIDTH, QHEIGHT = 1600, 900
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    ori_screen = pg.Surface((QWIDTH, QHEIGHT))

    mode = 'main'
    choose = 0
    Match = 0
    Round = 1
    Phase = 0
    t, w = 0, -1
    connect_mode = 'Single'
    tf1, tf2 = 0, 0 # 조건부 작동되는 tick
    common = None
    Rule = [['Straight'], []]
    dd = []
    is_esc = False
    CWIDTH, CHEIGHT = WIDTH, HEIGHT
    CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT

    p1 = Player()
    p2 = Player()
    sp = SP()
    WAITING_TIME = 30

    # mode 변수에 따라 실행되는 코드가 달라짐
    while True:
        if mode == 'main': # 초록색 게임 시작 화면
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode, connect_mode, p1 = mouse_main((WIDTH, HEIGHT), (mode, connect_mode, p1))
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    is_esc = not is_esc
                    if is_esc == False:
                        CWIDTH, CHEIGHT = WIDTH, HEIGHT
                        CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False
            
            draw_main(ori_screen)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            clock.tick(60)
            pg.display.update()

        if mode == 'choose_key': # "반과 팀을 선택하세요 하는 화면"
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode = mouse_choose_key((WIDTH, HEIGHT), mode)
                    if mode == "get_match":
                        sp = SP(group = p1.group, team = p1.team)
                        sp.enroll_player() 
                if event.type == KEYDOWN:
                    p1, tf1, tf2 = key_choose_key(event, (p1, tf1, tf2))
                    if event.key == K_ESCAPE:
                        is_esc = not is_esc
                        if is_esc == False:
                            CWIDTH, CHEIGHT = WIDTH, HEIGHT
                            CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False
            
            tf1, tf2 = draw_choose_key(ori_screen, p1, (tf1, tf2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            
            clock.tick(60)
            pg.display.update()

        if mode == 'resume': # "choose key 랑 화면 공유함
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    mode = mouse_choose_key((WIDTH, HEIGHT),mode)
                    if mode == "get_match":
                        print(p1.group, p1.team)
                        sp = SP(p1.group, p1.team)
                        Match, Round, Phase = sp.get_MRP()
                        p1.card_list = sp.get_hand()
                        p1.pre = [sp.get_pre()]
                        p1.coin = sp.get_chips()
                        p2num = sp.get_opponent(Match) 
                        p2 = Player(p2num, sp.get_hand(p2num))
                        choose = 0
                        if Phase == 3:   # 3페이즈를 진행함 -> 교환 후 1페이즈로 가야함 (새로운 상대 찾기)
                            mode="exchange_delay"
                            continue
                        if Phase == 4 :
                            continue
                        t, w = 0, -1
                        p1.active_list = []
                        p1.showc = []
                        p1.Rank = ''
                        p2.Rank = ''
                        p1.isdd = False
                        p2.isdd = False
                        r1, r2, reward_coin = set_para(Match)
                        p1.Rule = [r1, r2]
                        p2.Rule = [r1, r2]
                        
                        p1.active_list = []
                        p2.active_list = []
                        p1.shown = sp.get_shown()
                        p2.shown = sp.get_shown(p2.team)
                        if Phase == 1: #1페이즈를 진행함 -> 2페이즈임
                            mode = 'play_delay'
                            tmp_showc = sp.get_playing(phase=1)
                            tmp_card_list = p1.card_list.copy()
                            for card in tmp_showc:
                                for c in tmp_card_list:
                                    if c.equals(card):
                                        p1.showc.append(c)
                                        del(tmp_card_list[tmp_card_list.index(c)])
                            choose = 1
                        elif Phase == 2: #2페이즈를 진행함 -> 3페이즈 or 1페이즈 
                            tmp_showc = sp.get_playing(phase=1) + sp.get_playing(phase = 2)
                            tmp_card_list = p1.card_list.copy()
                            for card in tmp_showc:
                                for c in tmp_card_list:
                                    if c.equals(card):
                                        p1.showc.append(c)
                                        del(tmp_card_list[tmp_card_list.index(c)])
                            
                            p2.showc = sp.get_playing(p2.team, 1) 
                            
                            common = sp.get_common(Round)                
                            p1.common = common
                            p2.common = common
                            p1.showc = [common] + p1.showc
                            p2.showc = [common] + p2.showc
                            mode = "play_delay"
                            t = 0

                        #Phase = Phase % 2 + 1 


                if event.type == KEYDOWN:
                    p1, tf1, tf2 = key_choose_key(event, (p1, tf1, tf2))
            
            tf1, tf2 = draw_choose_key(ori_screen, p1, (tf1, tf2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            
            clock.tick(60)
            pg.display.update()

        if mode == 'get_match':  # Finding player - 하는 화면
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    p1 = mouse_get_match((WIDTH, HEIGHT), p1)
            
            t = draw_get_match(ori_screen, p1, t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            if connect_mode == 'Single' and t == 180:
                if Phase % 2 == 0:
                    Match += 1
                    p2 = Player(0, random.sample(make_whole(), 6))
                mode = 'reset'
            
            if connect_mode == 'Multi' and t % WAITING_TIME == 0:
                if sp.get_start_permission(Match+1) :
                    if Phase % 2 == 0:
                        Match += 1 
                        p2num = sp.get_opponent(Match) 
                        p2 = Player(p2num, sp.get_hand(p2num))
                    mode = 'reset'
                    # Phase = Phase%2 + 1

            clock.tick(60)
            pg.display.update()   

        if mode == 'reset': # 죽일 수 있는 모드인줄 알았는데, 역시 잘 돌아가는 코드는 건들면 안됨. 이름만 init => reset으로 바꿈.

            # 이쯤.. sp.get_hand가 실행되기 전에 적용해야 하는 아이템 효과가 있으므로
            if p1.using_item >= 0: p1.item[p1.using_item] -= 1
            sp.upload_item(p1)

            choose = 0
            t, w = 0, -1
            #p1, Match = start(Round, (p1, Match)) # 이 부분 대신에 DB에서 끌고 와야 하지
            if Match == 1 and Round == 1:
                if connect_mode == 'Single': p1.card_list = random.sample(make_whole(), 6)
            if connect_mode == 'Multi': p1.card_list = sp.get_hand()
            p1.active_list = []
            p1.showc = []
            p1.Rank = ''
            p2.Rank = ''
            p1.isdd = False
            p2.isdd = False
            if Round == 1:
                p1.pre.append([])
                p2.pre.append([])
            r1, r2, reward_coin = set_para(Match)
            p1.Rule = [r1, r2]
            p2.Rule = [r1, r2]
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
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    p1, p2, mode, choose, t, tf1 = mouse_play((WIDTH, HEIGHT), (p1, p2, mode, choose, t, tf1))
                    if mode == 'play_delay':
                        Phase = 2 if Phase == 1 else 1
                        if connect_mode == 'Multi':
                            sp.upload_playing( hand_cards = p1.active_list, match = Match, round = Round, phase = Phase)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    is_esc = not is_esc
                    if is_esc == False:
                        CWIDTH, CHEIGHT = WIDTH, HEIGHT
                        CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False

            p1, p2, t = draw_play(ori_screen, (Round, Match, choose, tf1), (p1, p2, t))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            if tf1: tf1 -= 1

            if choose == 0.5: choose = 1
            clock.tick(60)
            pg.display.update()
        
        if mode == 'play_delay': #여기에 대기시간 화면 필요 -> 페이즈 1 내고 상대 내는거까지 기다리는 시점
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE: is_esc = not is_esc
            
            t = draw_play_delay(ori_screen, (p1, p2), t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))

            if connect_mode == 'Single' and t == 60:
                if Phase == 1:
                    p2.showc = random.sample(p2.card_list, 2)
                    mode = 'flop'
                    t = 0
                else:
                    while True:
                        add_showc = random.sample(p2.card_list, 2)
                        if not add_showc[0] in p2.showc and not add_showc[1] in p2.showc: break
                    p2.showc += add_showc
                    mode = "result"
                    t = 0
                p1.active_list = []
                p2.active_list = []
            
            if connect_mode == 'Multi' and t % WAITING_TIME == 0 :
                if sp.has_conducted(p2.team,Match, Round, Phase):
                    #p2.active_list = sp.get_playing(p2.team, Phase)
                    if Phase == 1:
                        p2.showc = sp.get_playing(p2.team, Phase)
                        mode = 'flop'
                        t = 0
                    else:
                        p2.showc += sp.get_playing(p2.team, Phase)
                        mode = "result"
                        t = 0 
                    p1.active_list = []
                    p2.active_list = []
                    print(f"P2.showc :: {p2.showc}")
                
            clock.tick(60)
            pg.display.update()
            
        if mode == 'flop': # 카드 내는 애니메이션 
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if t >= 80 and event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode, p1, p2, t = mouse_flop((WIDTH, HEIGHT), (mode, p1, p2, t))
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    is_esc = not is_esc
                    if is_esc == False:
                        CWIDTH, CHEIGHT = WIDTH, HEIGHT
                        CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False
            
            t = draw_flop(ori_screen, (Round, Match, p1, p2), t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            
            if t == 60:
                if connect_mode == 'Single': common = get_random_card()
                if connect_mode == 'Multi': common = sp.get_common(Round)                
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
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode, Round, t, choose, p1, p2 = mouse_result((WIDTH, HEIGHT), (mode, Round, t, choose, p1, p2))
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    is_esc = not is_esc
                    if is_esc == False:
                        CWIDTH, CHEIGHT = WIDTH, HEIGHT
                        CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False
                
            if t == 0:
                p1.set_shown()
                sp.upload_shown(p1.shown)
                p2.set_shown()
                w = win(p1, p2)
            if t == 70:
                if w == 0: #무승부
                    p1.coin += (reward_coin // 2)
                    p1.pre[-1].append(0)
                    #p2.pre[-1].append(0)
                if w == 1: #승리
                    p1.coin += reward_coin
                    p1.pre[-1].append(1)
                    #p2.pre[-1].append(-1)
                if w == 2: #패배
                    p1.pre[-1].append(-1)
                    #p2.pre[-1].append(1)
                sp.update_cell('chips', p1.team+1, p1.coin)
                sp.upload_pre(p1.pre)
                #sp.clear_phase()
            if mode == 'result': #가끔 씹힐때 있어서 버그처리
                p1, p2, t = draw_result(ori_screen, (Round, Match, w), (p1, p2, t))
                screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
                if is_esc:
                    draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
                
                clock.tick(60)
                pg.display.update()
            
        if mode == 'exchange_lose': # 2패시 카드 고르는 단계
            for event in pg.event.get():
                if event.type == QUIT:   
                    pg.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode, choose, tf1, p1, p2 = mouse_exchange_lose((WIDTH, HEIGHT), (mode, choose, tf1, p1, p2))
                    if connect_mode == 'Multi' and mode == "exchange_result" : 
                        sp.update_cell('changed_index', p1.team+1, p1.ex_index)
                        sp.update_cell('changed_index', p2.team+1, p2.ex_index)
                        sp.update_cell("phase", p1.team+1, 3, False)
                        sp.update_cell("phase", p2.team+1, 3, False)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    is_esc = not is_esc
                    if is_esc == False:
                        CWIDTH, CHEIGHT = WIDTH, HEIGHT
                        CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False
            
            p1, p2 = draw_exchange_lose(ori_screen, (Match, choose, tf1), (p1, p2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
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
                if event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode, t, tf1, p1, p2 = mouse_exchange_draw((WIDTH, HEIGHT), (mode, t, tf1, p1, p2))
                    if connect_mode == 'Multi' and mode == "exchange_delay":
                        sp.update_cell("changed_index", p2.team+1, p2.ex_index)
                        sp.update_cell("phase", p1.team+1, 3, False)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    is_esc = not is_esc
                    if is_esc == False:
                        CWIDTH, CHEIGHT = WIDTH, HEIGHT
                        CQWIDTH, CQHEIGHT = QWIDTH, QHEIGHT
                if event.type == MOUSEBUTTONDOWN and is_esc:
                    (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT), ok_flag = set_screen_condition(screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
                    if ok_flag:
                        if CWIDTH == WIDTH and CHEIGHT == HEIGHT and CQWIDTH == QWIDTH and CQHEIGHT == QHEIGHT: pass # 진짜 pass임.
                        else:
                            WIDTH, HEIGHT = CWIDTH, CHEIGHT
                            QWIDTH, QHEIGHT = CQWIDTH, CQHEIGHT
                            pg.display.quit()
                            screen = pg.display.set_mode((WIDTH, HEIGHT))
                        is_esc = False
            
            p1, p2 = draw_exchange_draw(ori_screen, (Match, tf1), (p1, p2))
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
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

            if connect_mode == 'Single' and t == 60:
                if sum(p1.pre[-1]) > 0:
                    p1.ex_index = random.randint(0, len(p1.card_list)-1) # shown 정책 적용안해
                    p2.ex_index = random.randint(0, len(p2.card_list)-1)
                    p1.ex_card = p1.card_list[p1.ex_index]
                    p2.ex_card = p2.card_list[p2.ex_index]
                    choose = 0
                    t = 0
                    mode = 'exchange_result'
                if sum(p1.pre[-1]) == 0:
                    p1.ex_index = random.randint(0, len(p1.card_list)-1)
                    p1.ex_card = p1.card_list[p1.ex_index]
                    choose = 0
                    t = 0
                    mode = 'exchange_result'

            if connect_mode == 'Multi' and t % WAITING_TIME == 0 and sp.has_conducted(p2.team,Match, 2, 3):
                p1.ex_index = int(sp.get_acell('changed_index', p1.team+1))
                p2.ex_index = int(sp.get_acell('changed_index', p2.team+1))
                p1.ex_card = p1.card_list[p1.ex_index]
                p2.ex_card = p2.card_list[p2.ex_index]
                choose = 0
                t = 0
                mode = 'exchange_result'
                
                # if sum(p1.pre[-1]) > 0 :
                #     p1.ex_index = int(sp.get_acell('changed_index', p1.team+1))
                #     p2.ex_index = int(sp.get_acell('changed_index', p2.team+1))
                #     p1.ex_card = p1.card_list[p1.ex_index]
                #     p2.ex_card = p2.card_list[p2.ex_index]
                #     choose = 0
                #     t = 0
                #     mode = 'exchange_result'
                # if sum(p1.pre[-1]) == 0:
                #     p1.ex_index = int(sp.get_acell('changed_index', p1.team+1))
                #     p1.ex_card = p1.card_list[p1.ex_index]
                #     choose = 0
                #     t = 0
                #     mode = 'exchange_result'
                # if sum(p1.pre[-1]) < 0:
                #     choose = 0
                #     t = 0
                #     mode = 'exchange_result'
            clock.tick(60)
            pg.display.update()

        if mode == 'exchange_result': #교환 후 결과 보여주는 화면
            for event in pg.event.get():
                if event.type == QUIT:
                    pg.quit()
                    sys.exit()
                if t >= 90 and event.type == MOUSEBUTTONDOWN and not is_esc:
                    mode, t = mouse_exchange_result((WIDTH, HEIGHT), (mode, t))
                    if connect_mode == 'Multi' and mode == "get_match":
                        sp.upload_hand(hand_cards = p1.card_list)

            if t == 50:
                p1.card_list[p1.ex_index] = p2.ex_card
                p2.card_list[p2.ex_index] = p1.ex_card
            
            t = draw_exchange_result(ori_screen, (Match, p1, p2, choose), t)
            screen.blit(pg.transform.scale(ori_screen, (WIDTH, HEIGHT)), (0, 0))
            if is_esc:
                draw_option(ori_screen, (CWIDTH, CHEIGHT), (CQWIDTH, CQHEIGHT))
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