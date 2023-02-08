from spreadsheet import SP
from obj import *
import copy
import random
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtGui

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
        self.sp = SP(num)
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
            if steps[0] != str(match-1) or steps[1] != "2" or steps[2] != "4" :
               #print(steps)
                return False
        return True
    
    def get_share_cards(self, match=1):
        cells = self.sp.get_cell_range('share_cards', 1, 2, self.num_players, use_player_sheet=False)
        res = [x.split("|")[match-1].split(",") for x in cells]
       #print(res)
        return res

    def match_setting(self, match = 0, test=False):
        if test or self.ck_match(match) :
            self.sp.update_cell_range('match_permission', 1, 2, self.num_players, [match]*self.num_players, use_player_sheet=False)
            self.sp.update_cell_range('common1', 2, 2, self.num_players, self.get_share_cards(match) )
            self.sp.update_cell_range("phase1", 2, 2, self.num_players, [["",""] for x in range(self.num_players)] )
            self.sp.update_cell_range("pre", 1, 2, self.num_players, [""] * self.num_players, True )

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
            self.sp.update_cell_range('match', 3, 2, self.num_players, [ [0,2,4] for x in range(self.num_players)  ], use_player_sheet=False )
            self.sp.update_cell_range("team", 1, 2, self.num_players, list(range(1,self.num_players+1)), False)
            self.sp.update_cell_range("match_permission", 1, 2, self.num_players, [0] * self.num_players, False)
            return True
        else:
            print("Not Enough Players")
            return False

    def clear_game(self):
        #게임 초기화하기
        # 게임 결과를 엑셀로 저장할까?
          
        player_table_col = 13
        director_table_col = 6
        player_l = [ [''] * player_table_col for x in range(self.num_players)]
        director_l = [ [''] * director_table_col for x in range(self.num_players)]
        items = [['0|0|0|0|0'] for x in range(self.num_players)]
        using_items = [['-1'] for x in range(self.num_players)]

        self.sp.update_cell_range(1, player_table_col, 2 + (self.num-1)*8, self.num_players, player_l)
        self.sp.update_cell_range(2, director_table_col, 2 + (self.num-1)*8, self.num_players, director_l, False)
        self.sp.update_cell_range('item', 1, 2 + (self.num-1)*8, self.num_players, items)
        self.sp.update_cell_range('using_item', 1, 2 + (self.num-1)*8, self.num_players, using_items)

    # def joker_penalty(self):
    #     teams = list(range(1,self.num_players+1))
    #     chips = list(map(int, self.sp.get_cell_range('chips', 1, 2, self.num_players)))
    #     hands = self.sp.get_cell_range("hand", 1, 2, self.num_players)
        
    #     res = []
    #     for i in range(self.num_players):
    #         c = int(chips[i] * ( 0.8 ** ((hands[i].count('0') // 2) + (hands[i].count('Black'))))    )
    #         res.append( c )
        
    #     self.sp.update_cell_range( "chips", 1, 2, self.num_players, res )

    def get_ranking(self):
        teams = list(range(1,self.num_players+1))
        chips = list(map(int, self.sp.get_cell_range('chips', 1, 2, self.num_players)))

        ranking = sorted( [ [x, y] for x, y in zip(teams, chips) ], key = lambda x : x[1], reverse=True  )      
       #print("RANKING : ")
       #print(ranking)
       #print("-"*50)
        return ranking

    def making_hand_reversed(self):
        cards = self.sp.get_cell_range('hand', 1, 2, self.num_players)
       #print("cards "*5)
       #print(cards)
        
        ret = [  "|".join([ ((x[:-1] + f"{x[1]}") if  (x[-1] == '0' or x[-1].find('Black') > -1)  else (x[:-1] +  f"{8 - int(x[-1])}")) for x in c.split('|') ]) for c in cards ]
       #print("returned"*10)
        self.sp.update_cell_range('hand', 1, 2, self.num_players, ret)
        return ret

    def assign_item(self, team, item):
        items = list(map(int, self.sp.get_acell('item', team+1).split('|')))
        items[item] += 1
        items_str = "|".join(list(map(str, items)))
        self.sp.update_cell('item', team+1, items_str)

form_class = uic.loadUiType("DirectorQT.ui")[0]

class DirectorQT(QMainWindow, form_class): #QT로 만든 Director 프로그램
    #dr = None 
    dr = Director(1, NUMBER_OF_TEAMS)
    num_players = NUMBER_OF_TEAMS
    EXPLAINED = 2
    

    def __init__(self):
        #초기 설정
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("도둑포커 디렉터용 파일")
        
        #버튼에 기능 연결
        self.btn_matchStart.clicked.connect(self.btn_match_start)
        self.btn_mkItem.clicked.connect(self.btn_mk_item)
        
    def btn_mk_item(self):
        item      = self.get(self.cbox_itemNum, ob_type = "cbox")
        item_team = self.get(self.cbox_itemTNum, ob_type = "cbox")
        group     = self.get(self.txt_group)

        self.dr = Director(group, self.num_players)
        self.group = group
        self.dr.assign_item(item_team, item)

    def btn_match_start(self):
        group = self.get(self.txt_group)
        match = self.get(self.txt_matchNum)
        FINAL_MATCH = 15
        EXPLAIN_INFO = [1,4,8,11]

        if match <= 0:
            self.dr = Director(group, self.num_players)
            self.group = group

            if match == 0:
                self.dr.clear_game()
            self.set_text(self.txt_matchNum, 1)
            self.warning("다들 입장해주세요!")
        else:
            if self.dr is None:
                self.warning("초기화를 진행해주세요")
                return
            if match == 1 :
                if self.dr.sp.ck_players(self.num_players):
                    self.dr.game_setting()
                else: 
                    self.warning("아직 등록하지 않은 팀이 있습니다!")
                    return
            elif not self.dr.ck_match(match):
                self.warning("아직 진행되지 않은 팀이 있습니다!")
                return
            
            if match == FINAL_MATCH:
                # self.dr.joker_penalty()
                self.update_ranking()
                return
            SHOW_CHIPS = [ True if x < 11 else False for x in range(FINAL_MATCH+1)  ]
            SHOW_CHIPS[-1] = True
            self.update_ranking(show_chips= SHOW_CHIPS[match])
            if match in EXPLAIN_INFO:
                if self.EXPLAINED == 0: #바뀌는 룰과 아이템 설명 완료
                    self.EXPLAINED = 2
                    if match == EXPLAIN_INFO[3]:
                        self.dr.making_hand_reversed()

                elif self.EXPLAINED == 2:  
                    self.warning("미니게임 진행 후 아이템 저장을 완료해주세요!")
                    self.EXPLAINED = 1
                    item = self.get(ob=self.cbox_itemNum, ob_type='cbox')
                    print("ITEM : ", item)
                    self.set_image(self.img_explain, f'./explain_img{item}.png')
                    
                    return
                elif self.EXPLAINED == 1:
                    self.EXPLAINED = 0
                    self.warning("바뀐 룰을 확인해주세요!")
                    self.set_image(self.img_Jokbo, f'./Jokbo_img{match}.png')
                    return
            

            self.dr.match_setting(match)
            self.warning(f"{match}번 매치 진행")
            
            self.set_text(self.txt_matchNum, match+1)
      

    def update_ranking(self, show_chips = True):

        tb = self.table_ranking

        tb.setColumnCount(2)
        tb.setRowCount(self.num_players)
        tb.clear()
        tb.setFont(QtGui.QFont('맑은 고딕', 30))
        tb.setHorizontalHeaderLabels(["Team","Chips"])
        ranking = self.dr.get_ranking()
        
        for row, rank in enumerate(ranking):
            for col, val in enumerate(rank):
                val = val if show_chips else "비밀!"
                tb.setItem(row,col,QTableWidgetItem(str(val)))


    def set_image(self, ob, img_link=""):
        ob.setPixmap(QtGui.QPixmap(img_link))

    def set_text(self, ob, text="", ob_type="text"  ): # 값 설정
        if ob_type=="text":
            ob.setText(str(text))
            return True
        elif ob_type=="cbox":
            return False

    def get(self, ob, ob_type="text", clear=False, toint = True): #값 return
        if ob_type=="text":
            s = ob.text().strip()
        elif ob_type=="cbox":
            s = ob.currentText()
        if clear==True:
            ob.clear()

        if toint: s = int(s)
        return s
    def warning(self, text = "", title="알림"):
        QMessageBox.about(self,title,text)

if __name__ == "__main__" :
    app = QApplication(sys.argv) 

    myWindow = DirectorQT() 

    myWindow.show()

    app.exec_()
    
    
    # d = Director(1, num_players=int(input("플레이어 수 입력 : ")))
    # #d.clear_game()

    # #d.game_setting(test=True)
    # rec = -5
    # while True:
    #     a = int(input("match 값 입력하기 : "))
    #     if a == 0: break
    #     if a == -2: 
    #         d.clear_game()
    #     elif a == -1:
    #         d.game_setting(test=True)
    #         d.match_setting(1)
    #     elif a == -4:
    #         d.joker_penalty()
    #     elif a == -5:
    #         print(d.get_ranking()) 
    #     elif a == -6:
    #         print(d.making_hand_reversed())
    #     elif a == -3:
    #         if rec == -5 : 
    #             rec = -2
    #         while True:
    #             if rec == 0:
    #                 rec = 2
    #             if rec == -2: 
    #                 d.clear_game()
    #                 rec += 1
    #             elif rec == -1:
    #                 if d.game_setting(test=False):
    #                     rec += 1
    #             else:
    #                 if d.match_setting(rec):
    #                     rec += 1      
    #             print(rec)
    #             time.sleep(1)      
    #     else:
    #         d.match_setting(a, test=True)
    #     rec = a
