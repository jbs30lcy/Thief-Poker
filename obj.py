# obj 파일 : 모든 파일에서 필요한 기초 오브젝트를 구현해 놓음.
# 색상, 파일 경로, 카드 이미지 집합, Card class, Player class

import pygame as pg
import os
import random

White  = (255, 255, 255)
Black  = (0, 0, 0)
Red    = (240, 26, 0)
Pink   = (255, 180, 180)
RedG   = (177, 123, 116)
Yellow = (210, 190, 0)
Green  = (60, 179, 113)
GreenG = (101, 132, 115)
Blue   = (24, 160, 230)
Grey1  = (200, 200, 200)
Grey2  = (230, 230, 230)
Grey3  = (80, 80, 80)
Grey4  = (127, 127, 127)
GreyA  = (127, 127, 127, 127)
GreyB  = (80, 80, 80, 235)
GreyC  = (60, 60, 60, 240)
Brown1 = (227, 181, 140)

Card_IMGlist = {}
CI_half = {}
CI_std = {}
colors = ("Black", "Red", "Yellow", "Blue", "Green")
colors_dict = {"Black":0, "Red":1, "Yellow":2, "Blue":3, "Green":4}
NUMBER_OF_COLORS = 4
NUMBER_OF_NUM = 7

file_path = os.path.dirname(os.path.abspath(__file__))
img_dir_path = file_path + "/img/"

for color in colors[1:]:
    for num in range(1, 8):
        card_name = f"{color}_{num}"
        card_image = pg.transform.scale(pg.image.load(img_dir_path + card_name + ".png"), (600, 900))
        Card_IMGlist[card_name] = card_image
Card_IMGlist["Black"] = pg.transform.scale(pg.image.load(img_dir_path + "Black.png"), (600, 900))
Card_IMGlist["Hide"] = pg.transform.scale(pg.image.load(img_dir_path + "Hide.png"), (600, 900))

for card in Card_IMGlist:
    CI_half[card] = pg.transform.scale(Card_IMGlist[card], (300, 450))
    CI_std[card] = pg.transform.scale(Card_IMGlist[card], (180, 270))

MATCH_PARA = [
    [['Flush'], [], 20],
    [['Flush'], [4], 30],
    [['Straight', 'Flush', 'S-F'], [4], 30],
    [['Straight', 'Flush', 'S-F'], [4], 60]
]

Item_desc = [
    '?'
    '필요없는 카드 두 장을 랜덤한 카드 두 장으로 교체합니다.'
    '상대가 보유한 카드 중 랜덤으로 두 장을 엿볼 수 있습니다.'
    '이 매치에서 획득하는 코인이 두 배가 됩니다.'
    '다른 사람들이 가지고 있던 카드가 하나씩 전부 바뀝니다.'
]
Item_IMGlist = [pg.transform.scale(pg.image.load(img_dir_path + f"Item_{x}.png"), (160, 240)) for x  in range(5)]

def in_rect(pos, rect):
    return rect[0] <= pos[0] <= rect[0] + rect[2] and rect[1] <= pos[1] <= rect[1] + rect[3]

class Card:
    def __init__(self, color='00', val = 0, fromcell=False, use_random=False, except_joker=False):
        if use_random:
            ran = random.randrange(NUMBER_OF_COLORS * NUMBER_OF_NUM + 1)
            self.color = colors[(ran-1) // NUMBER_OF_NUM + 1 ]
            self.val = (ran-1) % NUMBER_OF_NUM + 1 if ran > 0 else 0
        elif fromcell:
            if type(color) == type(1):
                self.color = colors[color//10]
                self.val = int(color%10)
            elif len(color) <= 2: 
                self.color = colors[int(color[0]) ]
                self.val = int(color[1])
            else:
                self.color = color[:-1]
                self.val = int(color[-1])
        else:
            self.color = color
            self.val = val
        self.dd = []
        if self.color == 'Black': self.name = 'Black'
        else: self.name = self.color + '_' + str(self.val)
        self.img = Card_IMGlist[self.name]
        self.img_half = CI_half[self.name]
        self.img_std = CI_std[self.name]

    def equals(self, o):
        return str(self) == str(o)
    
    def __repr__(self):
        if color == 'Black':
            return '==Card Black=='
        else:
            return f'==Card {self.color} {self.val}=='
    
    def __str__(self):
        return f'{ colors_dict[self.color] }{self.val}'

    @staticmethod
    def rand_card(except_joker=False):
        ran = random.randrange(1 if except_joker else 0, NUMBER_OF_COLORS * NUMBER_OF_NUM + 1)
        
        color = colors[(ran-1) // NUMBER_OF_NUM + 1 ]
        val = (ran-1) % NUMBER_OF_NUM + 1 if ran > 0 else 0
            
        return f'{color}{val}'

    @classmethod
    def shrink(cls, surf, rate = 0.5):
        return pg.transform.scale(surf, (rate * surf.get_width(), rate * surf.get_height()))

class Player:
    def __init__(self, team = 1, card_list = [], group = 1):
        self.card_list = card_list
        self.active_list = []
        self.showc = []
        self.shown = []
        self.coin = 100
        self.common = None
        self.Rule = [['Flush'], []] # 일단 이걸로.
        self.dd = []
        self.Rank = ''
        self.isdd = False
        self.group = group
        self.team = team
        self.ex_index = 0
        self.ex_card = None
        self.pre = []
        self.item = [1, 1, 1, 1, 1]
        self.using_item = -1

    # str2score: 족보가 적혀 있는 str을 int로 변환하는 함수.
    def str2score(self, s):
        if 'Straight-Flush' in s:
            return 700 + 10 * int(s[0])
        if 'Four of a kind' in s:
            return 600 + 10 * int(s[0])
        if 'Straight' in s:
            return 500 + int(s[0])
        if 'Flush' in s:
            return 400 + int(s[s.find('(')+1 : s.find(')')])
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
        black_str = 'Black' if black > 0 else ''
        value_arr = [0]*7
        value_bool_arr = [0]*7
        color_arr = [0]*4
        for card in arr:
            if card.color == 'Black': continue
            value_arr[card.val - 1] += 1
            value_bool_arr[card.val - 1] = 1
            color_arr[colors_dict[card.color] - 1] += 1
        
        if 'S-F' in self.Rule[0]: # 스티플
            is_straight = False
            is_s_index = -1
            for i in range(3, -1, -1):
                slice_val_arr = value_bool_arr[i:i+4]
                if sum(slice_val_arr) + black == 4:
                    is_straight = True
                    is_s_index = i
            if is_straight and max(color_arr) + black == 4:
                n = ''.join(map(str, color_arr)).rindex(str(max(color_arr)))
                return f"{is_s_index+4} {colors[int(n)+1]} {black_str} Straight-Flush"
        if max(value_arr) + black == 4: # 포카드
            n = ''.join(map(str, value_arr)).rindex(str(max(value_arr)))
            return f"{int(n)+1} {black_str} Four of a kind"
        if 'Straight' in self.Rule[0]: # 스트레이트
            for i in range(3, -1, -1):
                slice_val_arr = value_bool_arr[i:i+4]
                if sum(slice_val_arr) + black == 4:
                    return f"{i+4} {black_str} Straight"
        if 'Flush' in self.Rule[0] and max(color_arr) + black == 4: # 플러시
            n = ''.join(map(str, color_arr)).rindex(str(max(color_arr)))
            return f"{colors[int(n)+1]} {black_str} Flush ({sum( [value_arr[i] * (i+1) for i in range(7)] )})"
        if max(value_arr) + black == 3: # 트리플
            n = ''.join(map(str, value_arr)).rindex(str(max(value_arr)))
            return f"{int(n)+1} {black_str} Three of a kind"
        if tuple(sorted(value_arr)) == (0, 0, 0, 0, 0, 2, 2): # 투 페어
            n1 = ''.join(map(str, value_arr)).rindex('2')
            n2 = ''.join(map(str, value_arr)).index('2')
            return f"{n1+1}-{n2+1} Two pair"
        if max(value_arr) + black == 2: # 원 페어
            n = ''.join(map(str, value_arr)).rindex(str(max(value_arr)))
            return f"{int(n)+1} {black_str} Pair"
        return f"No rank ({sum( [value_arr[i] * (i+1) for i in range(7)] )})" # 개패

    # rank: 검정 카드를 포함한 족보를 계산하기 위한, _rrank의 wrapper 함수.
    def rank(self):
        if self.Rank: return self.Rank  # memoization
        R = 'No rank (1)'
        for i in range(5):
            black_in = 0
            new_showc = self.showc.copy()
            del new_showc[i]
            for j in range(4):
                card = new_showc[j]
                if card.color == 'Black': black_in += 1
            if black_in > 0:
                arr = new_showc.copy()
                result_s = self._rrank(arr, black_in)
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

        if self.str2score(R) < 200:
            for i in range(5):
                new_showc = self.showc.copy()
                if new_showc[i].color == 'Black':
                    self.isdd = False
                    break
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

    # rank2p : 두 장 족보
    def rank2p(self, arr):
        n1 = arr[0].val
        n2 = arr[1].val
        c1 = arr[0].color
        c2 = arr[1].color

        if c1 == 'Black':
            return f'{n2} Black Pair'
        if c2 == 'Black':
            return f'{n1} Black Pair'
        if n1 == n2:
            return f'{n1} Pair'
        return f'No rank ({n1+n2})'

    # rank3p : 세 장 족보
    def rank3p(self, arr):
        n1 = arr[0].val
        n2 = arr[1].val
        n3 = arr[2].val
        c1 = arr[0].color
        c2 = arr[1].color
        c3 = arr[2].color

        if c1 == 'Black':
            if n2 == n3: return f'{n2} Black Three of a kind'
            else: return f'{max(n2, n3)} Black Pair'
        if c2 == 'Black':
            if n1 == n3: return f'{n3} Black Three of a kind'
            else: return f'{max(n1, n3)} Black Pair'
        if c3 == 'Black':
            if n1 == n2: return f'{n1} Black Three of a kind'
            else: return f'{max(n1, n2)} Black Pair'
        if n1 == n2 == n3:
            return f'{n1} Three of a kind'
        if n1 == n2 or n1 == n3:
            return f'{n1} Pair'
        if n2 == n3:
            return f'{n2} Pair'
        return f'No rank ({n1+n2+n3})'

    def set_shown(self):
        #2페이즈에 낸걸로 뽑기
        # self.shown = self.showc[1:].copy()
        
        #냈던 카드 전부 뽑기
        for card in self.showc[1:]:
            for c2 in self.shown:
                if card.equals(c2):
                    break
            else: self.shown.append(card)

class Item:
    def __init__(self, num):
        self.num = num
        self.desc = Item_desc[num]

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")