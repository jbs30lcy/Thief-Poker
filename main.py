import pygame as pg
from pygame.locals import *
import sys, time

pg.init()
screen = pg.display.set_mode((1200, 900))
pg.display.set_caption("도둑 포커")
clock = pg.time.Clock()

White = (255, 255, 255)
Black = (0, 0, 0)
Red   = (240, 26, 0)
Grey1 = (200, 200, 200)
GreyA = (127, 127, 127, 127)
Card_IMGlist = {}
mode = 'init'
choose = 0
Round = 1

for color in ("Red", "Yellow", "Blue"):
    for num in range(1, 6):
        card_name = f"{color}_{num}"
        card_image = pg.transform.scale(pg.image.load("Thief Poker/img/" + card_name + ".png"), (180, 270))
        Card_IMGlist[card_name] = card_image

Card_IMGlist["Black"] = pg.transform.scale(pg.image.load("Thief Poker/img/Black.png"), (180, 270))
Hide_card = pg.transform.scale(pg.image.load("Thief Poker/img/Hide.png"), (180, 270))

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

class Card:
    def __init__(self, color, val = 6): # Black card val : 6
        self.color = color
        self.val = val
        if 1 <= self.val <= 5:
            self.img = Card_IMGlist[self.color + '_' + str(self.val)]
        else:
            self.img = Card_IMGlist['Black']
        self.show = False

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


p1 = Player()
p2 = Player()

AR = pg.font.SysFont('Arialrounded', 72)
ARs = pg.font.SysFont('Arialrounded', 24)
ARm = pg.font.SysFont('Arialrounded', 36)

Next_Button = pg.Surface((90, 60))
Next_Button.fill((227, 181, 140))
Next_Button_text = ARs.render('Next', True, Black)
Next_Button.blit(Next_Button_text, (18, 15))

while True:
    if mode == 'init':
        p1.active_list = []
        p1.showc       = []
        p2.active_list = []
        p2.showc       = []
        choose = 0
        if Round == 1:
            p1.card_list = []
            p2.card_list = []
            p1.card_list.append(Card('Red', 1))
            p1.card_list.append(Card('Red', 2))
            p1.card_list.append(Card('Yellow', 2))
            p1.card_list.append(Card('Blue', 2))
            p1.card_list.append(Card('Blue', 4))
            p1.card_list.append(Card('Blue', 5))
            p2.card_list.append(Card('Red', 4))
            p2.card_list.append(Card('Yellow', 2))
            p2.card_list.append(Card('Yellow', 3))
            p2.card_list.append(Card('Yellow', 3))
            p2.card_list.append(Card('Blue', 1))
            p2.card_list.append(Card('Black'))
        
        mode = 'phase1'
    
    if mode == 'phase1':
        if Round == 1:
            p2.active_list.append(p2.card_list[1])
            p2.active_list.append(p2.card_list[2])
        if Round == 2:
            p2.active_list.append(p2.card_list[3])
            p2.active_list.append(p2.card_list[5])
        mode = 'play'
    
    if mode == 'play':
        Alpha_screen = pg.Surface((1200, 900), pg.SRCALPHA)
        screen.fill(Grey1)
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
                        if len(p1.active_list) != 2:
                            print("Wrong number of cards")
                            pg.quit()
                            sys.exit()
                        else:
                            mode = 'phase2'
                            choose = 0.5
                            p1.showc = p1.active_list.copy()
                            p1.active_list = []
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

        if choose == 0:
            text = AR.render("Choose two cards", True, Black)
            for i in range(6):
                card = p1.card_list[i]
                screen.blit(card.img, (10 + i*200, 450))
                if card in p1.active_list:
                    pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
            for i in range(4):
                screen.blit(Card.shrink(Hide_card), ((400 + i*100, 300)))
            screen.blit(text, (300, 50))
            screen.blit(Next_Button, (800, 750))
        
        if choose == 1:
            text = AR.render("Choose another two cards", True, Black)
            for i in range(6):
                card = p1.card_list[i]
                screen.blit(card.img, (10 + i*200, 450))
                if card in p1.active_list:
                    pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
                if card in p1.showc:
                    pg.draw.rect(Alpha_screen, GreyA, (10 + i*200, 450, 180, 270))
            for i in range(4):
                if i < len(p2.showc):
                    card = p2.showc[i]
                    screen.blit(Card.shrink(card.img), (400 + i*100, 300))
                else:
                    screen.blit(Card.shrink(Hide_card), ((400 + i*100, 300)))
            screen.blit(text, (150, 50))
            screen.blit(Next_Button, (800, 750))

        text = ARs.render(f"round {Round}", True, Black)
        screen.blit(text, (20, 20))

        if choose == 0.5:
            choose = 1

        screen.blit(Alpha_screen, (0, 0))
        clock.tick(60)
        pg.display.update()

    if mode == 'phase2':
        screen.fill(Grey1)
        
        for card in p1.showc:
            if not card in p1.shown:
                p1.shown.append(card)
        for card in p2.showc:
            if not card in p2.shown:
                p2.shown.append(card)
        p2.showc = p2.active_list.copy()
        screen.blit(p1.showc[0].img, (310, 450))
        screen.blit(p1.showc[1].img, (510, 450))
        screen.blit(p2.showc[0].img, (310, 150))
        screen.blit(p2.showc[1].img, (510, 150))
        p1_text = ARs.render('My Card', True, Black)
        p2_text = ARs.render('Rival\'s Card', True, Black)
        screen.blits([ (p1_text, (720, 600)) , (p2_text, (720, 300)) ])

        pg.display.update()
        time.sleep(2)
        p2.active_list = []
        if Round == 1:
            p2.active_list.append(p2.card_list[3])
            p2.active_list.append(p2.card_list[4])
        if Round == 2:
            p2.active_list.append(p2.card_list[1])
            p2.active_list.append(p2.card_list[2])
        mode = 'play'

    if mode == 'result':
        screen.fill(Grey1)
        
        p2.showc = p2.showc + p2.active_list.copy()
        for card in p1.showc:
            if not card in p1.shown:
                p1.shown.append(card)
        for card in p2.showc:
            if not card in p2.shown:
                p2.shown.append(card)
        for i in range(4):
            screen.blit(p1.showc[i].img, (110 + 200*i, 450))
            screen.blit(p2.showc[i].img, (110 + 200*i, 150))
        p1_text = ARs.render(f'My Card : {p1.rank()}', True, Black)
        p2_text = ARs.render(f'Rival\'s Card : {p2.rank()}', True, Black)
        screen.blits([ (p1_text, (400, 740)) , (p2_text, (400, 100)) ])

        pg.display.update()
        time.sleep(1)

        w = win(p1, p2)
        if w == 0:
            rtext = ARm.render(f'DRAW', True, Black)
            p1.coin += 10
        if w == 1:
            rtext = ARm.render(f'YOU WIN', True, Black)
            p1.coin += 5
        if w == 2:
            rtext = ARm.render(f'YOU LOSE', True, Black)
        wx = 600 - rtext.get_rect().width / 2
        screen.blit(rtext, (wx, 820))

        pg.display.update()
        time.sleep(14)

        Round += 1
        mode = 'init'
        if Round == 3:
            mode = 'exchange'
            choose = 0
            p1.active_list = []
            p2.active_list = []

    if mode == 'exchange': # 교환 당할 때 mode도 따로 만들어야됨.
        screen.fill(Grey1)
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
                            choose = 1.5
        
        if choose == 0:
            text = AR.render("Choose my card", True, Black)
            for i in range(6):
                card = p1.card_list[i]
                screen.blit(card.img, (10 + i*200, 450))
                if card in p1.active_list:
                    pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
            screen.blit(text, (300, 50))
            screen.blit(Next_Button, (800, 750))
        
        if choose == 1:
            text = AR.render("Choose a card you want", True, Black)
            for i in range(6):
                card = p1.card_list[i]
                screen.blit(card.img, (10 + i*200, 450))
                if card in p1.active_list:
                    pg.draw.rect(screen, Red, (10 + i*200, 450, 180, 270), 2)
            for i in range(len(p2.shown)):
                card = p2.shown[i]
                screen.blit(card.img, (610 - 100 * len(p2.shown)+ i*200, 150))
                if card in p2.active_list:
                    pg.draw.rect(screen, Red, (610 - 100 * len(p2.shown)+ i*200, 150, 180, 270), 2)
            screen.blit(text, (200, 50))
            screen.blit(Next_Button, (800, 750))

        if choose == 2:
            mode = 'exchangeR'
            p1.card_list.remove(p1.active_list[0])
            p2.card_list.remove(p2.active_list[0])
            p1.card_list.append(p2.active_list[0])
            p2.card_list.append(p1.active_list[0])

        if choose == 0.5: choose = 1
        if choose == 1.5: choose = 2
        clock.tick(60)
        pg.display.update()

    if mode == 'exchangeR':
        screen.fill(Grey1)
        text = AR.render("Result", True, Black)
        for i in range(6):
            card = p1.card_list[i]
            screen.blit(card.img, (10 + i*200, 450))
        screen.blit(text, (500, 50))
        screen.blit(Next_Button, (800, 750))

        pg.display.update()
        time.sleep(15)
        pg.quit()
        sys.exit()