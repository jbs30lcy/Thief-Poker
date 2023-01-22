# set.py : UI가 표시되지 않고 즉시 넘어가는 mode는 입력을 받지 않기 때문에
# 따로 파일을 빼 놓았다.

import pygame as pg
import random
from obj import *

def make_whole():
    card_list = []
    card_list.append(Card('Black'))
    for color in ('Red', 'Yellow', 'Blue', 'Green'):
        for num in range(1, 8):
            card_list.append(Card(color, num))
    return card_list

def start(const, var):
    Round   = const
    player1 = var[0]
    player2 = var[1]
    Match   = var[2]

    player1.active_list = []
    player1.showc       = []
    player2.active_list = []
    player2.showc       = []
    player1.Rank = ''
    player2.Rank = ''

    if Round == 1:
        player1.pre.append([])
        player2.pre.append([]) # 얘는 이제 DB에서 갖고와야 하는 부분.
        player1.shown = []
        player2.shown = []
        Match += 1
        player2.key = random.randint(1, 999)

        if Match == 1:
            player1.key = random.randint(1, 999)
            while True:
                player1.card_list = random.sample(make_whole(), 6)
                n = 0
                for i in range(6):
                    if player1.card_list[i].color == 'black': n += 1
                if n <= 1: break

        while True:
            player2.card_list = random.sample(make_whole(), 6)
            n = 0
            for i in range(6):
                if player2.card_list[i].color == 'black': n += 1
            if n <= 1: break

    return (player1, player2, Match)


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

def get_random_card():
    return Card(random.choice(('Red', 'Yellow', 'Blue', 'Green')), random.randint(1, 7))

def get_dd(r2, dd):
    dd = [0, 0]
    if 1 in r2: dd[0] = Card(random.choice(('Red', 'Yellow', 'Blue', 'Green')), random.randint(1, 7))
    if 2 in r2: dd[1] = tuple( random.sample(('Red', 'Yellow', 'Blue', 'Green'), 2) )
    return dd

def get_random_exchange(player):
    return random.choice(player.card_list)

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")