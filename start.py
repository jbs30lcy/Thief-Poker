import pygame as pg
import random
from obj import *
def start(const, var):
    Round   = const
    player1 = var[0]
    player2 = var[1]

    p1b = p2b = False
    player1.active_list = []
    player1.showc       = []
    player2.active_list = []
    player2.showc       = []
    if Round == 1:
        player1.card_list = []
        player2.card_list = []
        for i in range(6):
            if not p1b and random.random() < 1/16:
                player1.card_list.append(Card('Black'))
                p1b = True
            else:
                player1.card_list.append(Card(random.choice(['Red', 'Yellow', 'Blue']), random.randint(1, 5)))
            if not p2b and random.random() < 1/16:
                player2.card_list.append(Card('Black'))
                p2b = True
            else:
                player2.card_list.append(Card(random.choice(['Red', 'Yellow', 'Blue']), random.randint(1, 5)))

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


if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")