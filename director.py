from spreadsheet import SP
from obj import Card
import copy
from spreadsheet import SP_DB

class Director():
    def __init__(self, num = 0, num_players = 8):
        self.num = num #반번호
        self.sp = SP_DB(num)
        self.num_players = num_players

    def init_hands(self, use_setting=False, order_players = []):
        res = []
        except_joker = False
        if use_setting:
            pass
        else:
            for i in range(self.num_players):
                res.append("|".join([ str(Card(use_random=True)) for x in range(6)]))

        return res

    def mk_opponents(self):
        opps = [copy.deepcopy([0]*(self.num_players-1)*2) for x in range(self.num_players) ]
        share_cards = [copy.deepcopy([0]*(self.num_players-1)*2) for x in range(self.num_players) ]
        
        q = []
        for i in range(self.num_players):
            for j in range(i+1,self.num_players):
                q.append((i,j))
        tmpq = []
        i = 0
        while i < len(q):
            a, b = q[i]
            
            if len(tmpq) == self.num_players :
                tmpq = []
            
            if a in tmpq or b in tmpq:
                q.remove((a,b))
                q.append((a,b))
                print(f"불가능 ({a},{b})", q)
                continue
            
            tmpq.append(a)
            tmpq.append(b)
            #print(q)
            #print(tmpq)
            i += 1
        q = q + q
        print("QUEUE : ",q)
        print("OPPONENTS : ",opps)
        for i in range(len(q)):
            
            a = i // (self.num_players//2) # match
            b = i % (self.num_players//2) # team

            t1, t2 = q[i]
            opps[t1][a] = t2+1
            opps[t2][a] = t1+1
            cd = Card.rand_card(True) + "," + Card.rand_card(True)
            share_cards[t1][a] = cd
            share_cards[t2][a] = cd

        opps = [ "|".join( map(str, x) )  for x in opps ]
        
        print("SHARE CARDS",share_cards)
        print("OPPONENTS : ", opps)
        shares = [ '|'.join(x) for x in share_cards ]


        return opps, shares
    
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
        else:
            print("아직 경기가 끝나지 않았습니다.")

    def game_setting(self, test=False):
        if test or self.sp.ck_players(self.num_players) : 
            print("GAME START")
            self.sp.update_cell_range('hand',1,  2, self.num_players,  self.init_hands())
            self.sp.update_cell_range('chips', 1, 2, self.num_players, [100] * self.num_players)
            opps, shares = self.mk_opponents()

            self.sp.update_cell_range('opponents',1, 2, self.num_players, opps, use_player_sheet=False)
            self.sp.update_cell_range('share_cards', 1, 2, self.num_players, shares, False)
            self.sp.update_cell_range('match', 3, 2, self.num_players, [ [0,2,3] for x in range(self.num_players)  ], use_player_sheet=False )
            self.sp.update_cell_range("team", 1, 2, self.num_players, list(range(1,self.num_players+1)), False)
            self.sp.update_cell_range("match_permission", 1, 2, self.num_players, [0] * self.num_players, False)
            self.match_setting(1, test)
        else:
            print("Not Enough Players")


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

    while True:
        a = int(input("match 값 입력하기 : "))
        if a == 0: break
        if a == -2: 
            d.clear_game()
        elif a == -1:
            d.game_setting(test=True)
        else:
            d.match_setting(a)

