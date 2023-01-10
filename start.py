import pygame as pg
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
        player1.card_list = []
        player2.card_list = []
        player1.card_list.append(Card('Red', 1))
        player1.card_list.append(Card('Red', 2))
        player1.card_list.append(Card('Yellow', 2))
        player1.card_list.append(Card('Blue', 2))
        player1.card_list.append(Card('Blue', 4))
        player1.card_list.append(Card('Blue', 5))
        player2.card_list.append(Card('Red', 4))
        player2.card_list.append(Card('Yellow', 2))
        player2.card_list.append(Card('Yellow', 3))
        player2.card_list.append(Card('Yellow', 3))
        player2.card_list.append(Card('Blue', 1))
        player2.card_list.append(Card('Black'))

    return (player1, player2)


def phase1(const, var):
    Round   = const
    player1 = var[0]
    player2 = var[1]
    if Round == 1:
        player2.active_list.append(player2.card_list[1])
        player2.active_list.append(player2.card_list[2])
    if Round == 2:
        player2.active_list.append(player2.card_list[3])
        player2.active_list.append(player2.card_list[5])
    return (player1, player2)


def phase2(const, var):
    Round   = const
    player1 = var[0]
    player2 = var[1]
    player1.active_list = []
    player2.active_list = []
    if Round == 1:
        player2.active_list.append(player2.card_list[3])
        player2.active_list.append(player2.card_list[4])
    if Round == 2:
        player2.active_list.append(player2.card_list[1])
        player2.active_list.append(player2.card_list[2])

    return (player1, player2)


if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")