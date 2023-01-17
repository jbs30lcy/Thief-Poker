# start.py : UI가 표시되지 않고 즉시 넘어가는 mode는 입력을 받지 않기 때문에
# 따로 파일을 빼 놓았다.

import pygame as pg
import random
from obj import *
def start(const, var):
    Round   = const
    player1 = var[0]
    player2 = var[1]

    player1.active_list = []
    player1.showc       = []
    player2.active_list = []
    player2.showc       = []
    if Round == 1:
        whole_card_list = []
        whole_card_list.append(Card('Black'))
        for color in ('Red', 'Yellow', 'Blue'):
            for num in range(1, 8):
                whole_card_list.append(Card(color, num))

        while True:
            player1.card_list = random.sample(whole_card_list, 6)
            n = 0
            for i in range(6):
                if player1.card_list[i].color == 'black': n += 1
            if n <= 1: break

        while True:
            player2.card_list = random.sample(whole_card_list, 6)
            n = 0
            for i in range(6):
                if player2.card_list[i].color == 'black': n += 1
            if n <= 1: break

    return (player1, player2)


def phase1(var):
    player2 = var

    x, y = random.sample(range(6), 2)
    player2.active_list.append(player2.card_list[x])
    player2.active_list.append(player2.card_list[y])
    return player2


def phase2(var):
    player1 = var[0]
    player2 = var[1]
    player1.active_list = []
    player2.active_list = []
    while True:
        x, y = random.sample(range(6), 2)
        if not player2.card_list[x] in player2.showc and not player2.card_list[y] in player2.showc: break
    player2.active_list.append(player2.card_list[x])
    player2.active_list.append(player2.card_list[y])
    return (player1, player2)

def get_common():
    return Card(random.choice(('Red', 'Yellow', 'Blue')), random.randint(1, 7))

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")