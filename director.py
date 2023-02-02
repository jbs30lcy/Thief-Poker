from spreadsheet import SP
from obj import Card
import copy
from spreadsheet import SP_DB
import random
import time

OPPO2 = [
    [(1, 2)]
]
OPPO4 = [
    [(1, 2), (3, 4)],
    [(1, 3), (2, 4)],
    [(1, 4), (2, 3)]
]
OPPO6 = [
    [(1, 2), (3, 4), (5, 6)],
    [(1, 3), (2, 5), (4, 6)],
    [(1, 4), (2, 6), (3, 5)],
    [(1, 5), (2, 4), (3, 6)],
    [(1, 6), (2, 3), (4, 5)]
]
OPPO8 = [
    [(1, 2), (3, 4), (5, 6), (7, 8)],
    [(1, 3), (2, 4), (5, 7), (6, 8)],
    [(1, 4), (2, 3), (5, 8), (6, 7)],
    [(1, 5), (2, 6), (3, 7), (4, 8)],
    [(1, 6), (2, 5), (3, 8), (4, 7)],
    [(1, 7), (2, 8), (3, 5), (4, 6)],
    [(1, 8), (2, 7), (3, 6), (4, 5)]
]
OPPO10 = [
    [(1, 2), (3, 4), (5, 6), (7, 8), (9, 10)],
    [(1, 3), (2, 4), (5, 7), (6, 9), (8, 10)],
    [(1, 4), (2, 3), (5, 8), (6, 10), (7, 9)],
    [(1, 5), (2, 6), (3, 7), (4, 10), (8, 9)],
    [(1, 6), (2, 5), (3, 8), (4, 9), (7, 10)],
    [(1, 7), (2, 8), (3, 9), (4, 6), (5, 10)],
    [(1, 8), (2, 9), (3, 10), (4, 5), (6, 7)],
    [(1, 9), (2, 10), (3, 5), (4, 7), (6, 8)],
    [(1, 10), (2, 7), (3, 6), (4, 8), (5, 9)]
]

def select_two_common():
    Card_list = []
    for color in ('Red', 'Blue', 'Yellow', 'Green'):
        for num in range(1, 8):
            Card_list.append(Card(color, num))
    return random.sample(Card_list, 2)

class Director():
    def __init__(self, num = 0, num_players = 8):
        self.num = num #반번호
        self.sp = SP_DB(num)
        self.num_players = num_players

    def init_hands(self, use_setting=False, order_players = []):
        res = []
        except_joker = False
        if use_setting:
            tmp = [ "00|11|23|24|16|47",
                    "00|41|12|14|35|26",
                    "00|21|32|13|34|45",
                    "42|33|34|15|46|37",
                    "22|14|25|46|37|17",
                    "31|31|22|13|45|26",
                    "32|23|44|15|16|27",
                    "41|12|43|24|36|47"]
            if order_players == []:
                order_players = list(range(self.num_players))
                random.shuffle(order_players)
            for i in order_players:
                res.append(tmp[i])
        else:
            for i in range(self.num_players):
                res.append("|".join([ str(Card(use_random=True)) for x in range(6)]))

        return res

    def mk_opponents(self):
        
        np = self.num_players
        opps = ['' for i in range(np)]
        shares = ['' for i in range(np)]

        for _ in range(2):
            for match in range(1, np):
                oppo_list = eval(f'OPPO{np}')[match-1]
                for n in range(1, np+1):
                    for i in range(np//2):
                        if oppo_list[i][0] == n:
                            card1, card2 = select_two_common()
                            opps[n-1] += f'{oppo_list[i][1]}|'
                            opps[oppo_list[i][1]-1] += f'{oppo_list[i][0]}|'
                            shares[n-1] += f'{card1.color}{card1.val},{card2.color}{card2.val}|'
                            shares[oppo_list[i][1]-1] += f'{card1.color}{card1.val},{card2.color}{card2.val}|'
                            
        
        return list(map(lambda x: x[:-1], opps)), list(map(lambda x: x[:-1], shares))
    
    def ck_match(self, match):
        cells = self.sp.get_cell_range('match', 3, 2, self.num_players, use_player_sheet=False)
        for steps in cells : 
            if steps[0] != str(match-1) or steps[1] != "2" or steps[2] != "3" :
                print(steps)
                return False
        return True
    
    def get_share_cards(self, match=1):
        cells = self.sp.get_cell_range('share_cards', 1, 2, self.num_players, use_player_sheet=False)
        res = [x.split("|")[match-1].split(",") for x in cells]
        print(res)
        return res

    def match_setting(self, match = 0, test=False):
        if test or self.ck_match(match) :
            self.sp.update_cell_range('match_permission', 1, 2, self.num_players, [match]*self.num_players, use_player_sheet=False)
            self.sp.update_cell_range('common1', 2, 2, self.num_players, self.get_share_cards(match) )
            self.sp.update_cell_range("phase1", 2, 2, self.num_players, [["",""] for x in range(self.num_players)] )
            
            print(f"{match}번 매치 시작")
            return True
        else:
            print("아직 경기가 끝나지 않았습니다.")
            return False

    def game_setting(self, test=False):
        if test or self.sp.ck_players(self.num_players) : 
            print("GAME START")
            self.sp.update_cell_range('hand',1,  2, self.num_players,  self.init_hands(use_setting=True))
            self.sp.update_cell_range('chips', 1, 2, self.num_players, [100] * self.num_players)
            opps, shares = self.mk_opponents()

            self.sp.update_cell_range('opponents',1, 2, self.num_players, opps, use_player_sheet=False)
            self.sp.update_cell_range('share_cards', 1, 2, self.num_players, shares, False)
            self.sp.update_cell_range('match', 3, 2, self.num_players, [ [0,2,3] for x in range(self.num_players)  ], use_player_sheet=False )
            self.sp.update_cell_range("team", 1, 2, self.num_players, list(range(1,self.num_players+1)), False)
            self.sp.update_cell_range("match_permission", 1, 2, self.num_players, [0] * self.num_players, False)
            self.match_setting(1, test)
            return True
        else:
            print("Not Enough Players")
            return False

    def clear_game(self):
        #게임 초기화하기
        # 게임 결과를 엑셀로 저장할까?    

        player_l = [ ['']*9 for x in range(self.num_players)]
        director_l = [ ['']*6 for x in range(self.num_players)]
        self.sp.update_cell_range(1, 9, 2 + (self.num-1)*8, self.num_players, player_l)
        self.sp.update_cell_range(2, 6, 2 + (self.num-1)*8, self.num_players, director_l, False)
        

if __name__ == "__main__" :
    d = Director(1, num_players=int(input("플레이어 수 입력 : ")))
    d.clear_game()

    #d.game_setting(test=True)
    rec = -5
    while True:
        a = int(input("match 값 입력하기 : "))
        if a == 0: break
        if a == -2: 
            d.clear_game()
        elif a == -1:
            d.game_setting(test=True)
        elif a == -3:
            if rec == -5 : 
                rec = -2
            while True:
                if rec == 0:
                    rec = 2
                if rec == -2: 
                    d.clear_game()
                    rec += 1
                elif rec == -1:
                    if d.game_setting(test=False):
                        rec += 1
                else:
                    if d.match_setting(rec):
                        rec += 1      
                time.sleep(1)      
        else:
            d.match_setting(a)
        rec = a
