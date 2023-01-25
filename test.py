from obj import *
import random

def make_whole():
    card_list = []
    card_list.append(Card('Black'))
    for color in ('Red', 'Yellow', 'Blue', 'Green'):
        for num in range(1, 8):
            card_list.append(Card(color, num))
    return card_list

epoch = 20000
p1 = Player()
p2 = Player()
p1.Rule = ['Flush', [4]]
p2.Rule = ['Flush', [4]]
CL = make_whole()
x, y = 0, 0
for i in range(epoch):
    p1.Rank = ''
    p2.Rank = ''
    p1.isdd = False
    p2.isdd = False
    p1.showc = random.sample(CL, 4)
    p2.showc = random.sample(CL, 4)
    common = random.choice(CL)
    while common.color == 'Black': common = random.choice(CL)
    p1.showc.append(common)
    p2.showc.append(common)
    _ = p2.rank()
    if 'Flush' in p1.rank():
        x += 1
        if p2.isdd:
            y += 1
    if i % (epoch // 100) == 0: print(str(round(i / epoch * 100, 1)) + '%')
print(x, y)