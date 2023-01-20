# obj 파일 : 모든 파일에서 필요한 기초 오브젝트를 구현해 놓음.
# 색상, 파일 경로, 카드 이미지 집합, Card class, Player class

import pygame as pg
import os

White  = (255, 255, 255)
Black  = (0, 0, 0)
Red    = (240, 26, 0)
RedG   = (177, 123, 116)
Yellow = (210, 190, 0)
Green  = (60, 179, 113)
GreenG = (101, 132, 115)
Blue   = (24, 160, 230)
Grey1  = (200, 200, 200)
Grey2  = (230, 230, 230)
Grey3  = (80, 80, 80)
GreyA  = (127, 127, 127, 127)
Brown1 = (227, 181, 140)
Grad1  = (40, 205, 147)
Grad2  = (40, 205, 198)
Grad3  = (40, 171, 205)
Grad4  = (40, 137, 205)
Card_IMGlist = {}


file_path = os.path.dirname(os.path.abspath(__file__))
img_dir_path = file_path + "\\img\\"

for color in ("Red", "Yellow", "Blue", "Green"):
    for num in range(1, 8):
        card_name = f"{color}_{num}"
        card_image = pg.transform.scale(pg.image.load(img_dir_path + card_name + ".png"), (180, 270))
        Card_IMGlist[card_name] = card_image

Card_IMGlist["Black"] = pg.transform.scale(pg.image.load(img_dir_path + "Black.png"), (180, 270))
Card_IMGlist["Hide"] = pg.transform.scale(pg.image.load(img_dir_path + "Hide.png"), (180, 270))

class Card:
    def __init__(self, color, val = 0):
        self.color = color
        self.val = val
        self.dd = []
        self.time = 5     # 카드의 수명 얘기 나와서요
        if 1 <= self.val <= 7:
            self.img = Card_IMGlist[self.color + '_' + str(self.val)]
        else:
            self.img = Card_IMGlist['Black']
        self.show = False

    def __repr__(self):
        if color == 'Black':
            return '==Card Black=='
        else:
            return f'==Card {self.color} {self.val}=='


    @classmethod
    def shrink(cls, surf):
        return pg.transform.scale(surf, (90, 135))

class Player:
    def __init__(self):
        self.card_list = []
        self.active_list = []
        self.showc = []
        self.shown = []
        self.coin = 0
        self.common = None
        self.Rule = []
        self.dd = []
        self.Rank = ''
        self.isdd = False
        # self.key (Client를 구별할 요소)
        self.pre = [0]

    # str2score: 족보가 적혀 있는 str을 int로 변환하는 함수.
    def str2score(self, s):
        if 'Four of a kind' in s:
            return 500 + 10 * int(s[0])
        if 'Straight' in s:
            return 400 + int(s[0])
        if 'Flush' in s:
            return 400
        if 'Three of a kind' in s:
            return 300 + 10 * int(s[0])
        if 'Two pair' in s:
            return 200 + 7 * int(s[0]) + int(s[2])
        if 'Pair' in s:
            return 100 + 10 * int(s[0])
        if 'No rank' in s:
            return int(s[8:][1:][:-1])
    
    # _rrank: Card 객체 4개가 담긴 list인 arr을 확인해 str 형태의 족보로 반환하는 함수.
    def _rrank(self, arr, black):
        new_arr = arr.copy()
        new_arr.sort(key = lambda x: x.val)
        n1 = new_arr[0].val
        n2 = new_arr[1].val
        n3 = new_arr[2].val
        n4 = new_arr[3].val
        c1 = new_arr[0].color
        c2 = new_arr[1].color
        c3 = new_arr[2].color
        c4 = new_arr[3].color
        blacks = 'Black' if black == True else ''

        if n1 == n2 == n3 == n4:
            return f"{n1} {blacks} Four of a kind"
        if self.Rule[0] == 'Straight' and n1+3 == n2+2 == n3+1 == n4:
            return f"{n4} {blacks} Straight"
        if self.Rule[0] == 'Flush' and c1 == c2 == c3 == c4:
            return f"{c1} {blacks} Flush"
        if n1 == n2 == n3:
            return f"{n1} {blacks} Three of a kind"
        if n1 == n2 == n4:
            return f"{n1} {blacks} Three of a kind"
        if n1 == n3 == n4:
            return f"{n1} {blacks} Three of a kind"
        if n2 == n3 == n4:
            return f"{n2} {blacks} Three of a kind"
        if n1 == n2 and n3 == n4:
            return f"{max(n1, n3)}-{min(n1, n3)} {blacks} Two pair"
        if n1 == n3 and n2 == n4:
            return f"{max(n1, n2)}-{min(n1, n2)} {blacks} Two pair"
        if n1 == n4 and n2 == n3:
            return f"{max(n1, n2)}-{min(n1, n2)} {blacks} Two pair"
        if n1 == n2 or n1 == n3 or n1 == n4:
            return f"{n1} {blacks} Pair"
        if n2 == n3 or n2 == n4:
            return f"{n2} {blacks} Pair"
        if n3 == n4:
            return f"{n3} {blacks} Pair"
        return f"No rank ({n1+n2+n3+n4})"

    # rank: 검정 카드를 포함한 족보를 계산하기 위한, _rrank의 wrapper 함수.
    def rank(self):
        if self.Rank: return self.Rank  # memoization
        R = 'No rank (1)'
        for i in range(5):
            black_in = False
            new_showc = self.showc.copy()
            del new_showc[i]
            for j in range(4):
                card = new_showc[j]
                if card.color == 'Black':
                    black_in = True
                    black_i = j
                    break
            if black_in:
                arr = new_showc.copy()
                max_s = ''
                max_score = 0
                for color in ('Red', 'Yellow', 'Blue', 'Green'):
                    for val in range(1, 8):
                        arr[black_i] = Card(color, val)
                        x = self._rrank(arr, black_in)
                        if self.str2score(x) > max_score:
                            max_score = self.str2score(x)
                            max_s = x
                result_s = max_s
                result_isblack = True
            else:
                result_s = self._rrank(new_showc, black_in)
                result_isblack = False

            rs = self.str2score(result_s)
            Rs = self.str2score(R)
            if rs > Rs:
                R = result_s
            elif rs == Rs and not result_isblack:
                R = result_s

        Is_black = False
        for i in range(5):
            card = self.showc[i]
            if card.color == 'black':
                Is_black = True
                break
        if not Is_black:
            for i in range(5):
                new_showc = self.showc.copy()
                del new_showc[i]
                self.isdd = self.set_isdd(new_showc, R)

        self.Rank = R
        return R

    def set_isdd(self, arr, rrank):
        if self.isdd: return True
        if 1 in self.Rule[1] and 'No rank' in rrank:
            for card in arr:
                if card.color == self.dd[0].color and card.val == self.dd[0].val:
                    return True
        if 2 in self.Rule[1] and 'Pair' in rrank:
            for i, j in [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]:
                card1 = arr[i]
                card2 = arr[j]
                if card1.val == card2.val and card1.color in self.dd[1] and card2.color in self.dd[1]:
                    return True
        if 4 in self.Rule[1] and self.str2score(rrank) < 200:
            color_arr = list(map(lambda x: x.color, arr))
            color_arr.sort()
            if tuple(color_arr) == ('Blue', 'Green', 'Red', 'Yellow'):
                return True
        return False


if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")