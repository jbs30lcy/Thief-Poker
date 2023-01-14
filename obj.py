import pygame as pg
import os

White  = (255, 255, 255)
Black  = (0, 0, 0)
Red    = (240, 26, 0)
Yellow = (210, 190, 0)
Blue   = (24, 160, 230)
Grey1  = (200, 200, 200)
Grey2  = (230, 230, 230)
GreyA  = (127, 127, 127, 127)
Card_IMGlist = {}

file_path = os.path.dirname(os.path.abspath(__file__))
img_dir_path = file_path + "\\img\\"

for color in ("Red", "Yellow", "Blue"):
    for num in range(1, 6):
        card_name = f"{color}_{num}"
        card_image = pg.transform.scale(pg.image.load(img_dir_path + card_name + ".png"), (180, 270))
        Card_IMGlist[card_name] = card_image

Card_IMGlist["Black"] = pg.transform.scale(pg.image.load(img_dir_path + "Black.png"), (180, 270))
Card_IMGlist["Hide"] = pg.transform.scale(pg.image.load(img_dir_path + "Hide.png"), (180, 270))

class Card:
    def __init__(self, color, val = 6): # Black card val : 6
        self.color = color
        self.val = val
        if 1 <= self.val <= 5:
            self.img = Card_IMGlist[self.color + '_' + str(self.val)]
        else:
            self.img = Card_IMGlist['Black']
        self.show = False

    def __str__(self):
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
        #self.pre(전적)
    def str2score(self, s):
        sign = -1 if 'Black' in s else 1
        if 'Four of a kind' in s:
            return sign * (500 + 10 * int(s[0]))
        if 'Flush' in s:
            return sign * 400
        if 'Three of a kind' in s:
            return sign * (300 + 10 * int(s[0]))
        if 'Two pair' in s:
            return sign * (200 + 5 * int(s[0]) + int(s[2]))
        if 'Pair' in s:
            return sign * (100 + 10 * int(s[0]))
        if 'No rank' in s:
            return int(s[8:][1:][:-1])
        
    def _rrank(self, arr, black):
        n1 = arr[0].val
        n2 = arr[1].val
        n3 = arr[2].val
        n4 = arr[3].val
        c1 = arr[0].color
        c2 = arr[1].color
        c3 = arr[2].color
        c4 = arr[3].color
        blacks = 'Black' if black == True else '' 
        #print(n1, c1, n2, c2, n3, c3, n4, c4)

        if n1 == n2 == n3 == n4:
            return f"{n1} {blacks} Four of a kind"
        if c1 == c2 == c3 == c4:
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

    def rank(self):
        black_in = False
        for i in range(4):
            card = self.showc[i]
            if card.color == 'Black':
                black_in = True
                black_i = i
                break
        if black_in:
            new_showc = self.showc.copy()
            max_s = ''
            max_score = 0
            for color in ('Red', 'Yellow', 'Blue'):
                for val in range(1, 6):
                    new_showc[black_i] = Card(color, val)
                    x = self._rrank(new_showc, black_in)
                    #print(x)
                    if abs(self.str2score(x)) > max_score:
                        max_score = abs(self.str2score(x))
                        max_s = x
            x = self._rrank(self.showc, black_in)
            if abs(self.str2score(x)) > max_score:
                max_score = self.str2score(x)
                max_s = x
            return max_s
        else:
            return self._rrank(self.showc, black_in)


if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")