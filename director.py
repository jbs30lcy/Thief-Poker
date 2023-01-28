from spreadsheet import SP
from obj import Card
import copy

class Director():
    def __init__(self, num = 0, num_players = 8):
        self.num = num #반번호
        self.sp = SP(num)
        self.num_players = num_players

    def init_hands(self, use_setting=False, order_players = []):
        res = []
        except_joker = False
        if use_setting:
            pass
        else:
            for i in range(self.num_players):
                res.append([ Card(use_random=True) for x in range(6)])
        return res

    def mk_opponents(self):
        opps = [copy.deepcopy([0]*(self.num_players-1)) for x in range(self.num_players) ]
        share_cards = [copy.deepcopy([0]*(self.num_players-1)) for x in range(self.num_players) ]
        
        q = []
        for i in range(self.num_players):
            for j in range(i+1,self.num_players):
                q.append((i,j))
        tmpq = []
        i = 0
        while i < len(q):
            a, b = q[i]
            
            if i % 4 == 0 :
                tmpq = []
            
            if a in tmpq or b in tmpq:
                q.remove((a,b))
                q.append((a,b))
                #print(f"불가능 ({a},{b})")
                continue
            
            tmpq.append(a)
            tmpq.append(b)
            #print(q)
            #print(tmpq)
            i += 1
        #print(q)
        #print(opps)
        for i in range(len(q)):
            a = i // 4 
            b = i % 4 
            
            opps[q[i][1]][a] = q[i][0] + 1
            opps[q[i][0]][a] = q[i][1] + 1
            cd = Card.rand_card(True) + "," + Card.rand_card(True)
            share_cards[b*2][a] = cd 
            share_cards[b*2+1][a] = cd

        # for i in range(1,self.num_players):
        #     for j in range(1,self.num_players+1):
        #         oppo = ( i + j - 1) % self.num_players + 1
        #         #print(oppo)
        #         if opps[j-1][i-1] == 0 and opps[oppo-1][i-1] == 0 : 
        #             opps[j-1][i-1] = oppo
        #             opps[oppo-1][i-1] = j
        #             cd = Card.rand_card(True) + "," + Card.rand_card(True)
        #             share_cards[j-1][i-1] = cd
        #             share_cards[oppo-1][i-1] = cd
                #print(opps)

        print(share_cards)
        shares = [ '|'.join(x) for x in share_cards ]
        if self.num_players == 2 :
            opps = [x[0] for x in opps]
        

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
        return [x.split("|")[match-1].split(",") for x in cells]


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
            self.sp.update_cell_range(self.sp.cols['hand'], 6, 2, self.num_players, self.init_hands())
            self.sp.update_cell_range(self.sp.cols['chips'], 1, 2, self.num_players, [100] * self.num_players)
            opps, shares = self.mk_opponents()

            self.sp.update_cell_range('opponents', self.num_players-1, 2, self.num_players, opps, use_player_sheet=False)
            self.sp.update_cell_range('share_cards', 1, 2, self.num_players, shares, False)
            self.sp.update_cell_range('match', 3, 2, self.num_players, [ [0,2,3] for x in range(self.num_players)  ], use_player_sheet=False )
            self.sp.update_cell_range("team", 1, 2, self.num_players, list(range(1,self.num_players+1)), False)
            self.sp.update_cell_range("match_permission", 1, 2, self.num_players, [0] * self.num_players, False)
        else:
            print("Not Enough Players")


    def clear_game(self):
        #게임 초기화하기
        # 게임 결과를 엑셀로 저장할까?    
        tmp = 15
        l = [ ['']*tmp for x in range(self.num_players)]
        
        self.sp.update_cell_range(1, tmp, 2, self.num_players, l)
        self.sp.update_cell_range(1, tmp, 2, self.num_players, l, False)
        

if __name__ == "__main__" :
    d = Director(num_players=int(input("플레이어 수 입력 : ")))
    d.clear_game()

    d.game_setting(test=True)

    while True:
        a = int(input("match 값 입력하기 : "))
        if a == 0: break
        if a == -2 : 
            d.clear_game()
        elif a == -1:
            d.game_setting(test=True)
        else:
            d.match_setting(a)

