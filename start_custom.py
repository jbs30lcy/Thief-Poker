# start_custom.py : 카드를 나눠주는 작업을 조작하기 위해 만든 파일. (start.py와 구조 비슷함)
# 사용하지 않는 파일이다.

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

        # ========== custom ==========
        player1.card_list.append(Card('Red', 1))
        player1.card_list.append(Card('Red', 2))
        player1.card_list.append(Card('Red', 3))
        player1.card_list.append(Card('Red', 4))
        player1.card_list.append(Card('Red', 5))
        player1.card_list.append(Card('Red', 6))
        player2.card_list.append(Card('Yellow', 1))
        player2.card_list.append(Card('Red', 2))
        player2.card_list.append(Card('Red', 3))
        player2.card_list.append(Card('Red', 4))
        player2.card_list.append(Card('Red', 5))
        player2.card_list.append(Card('Black'))
        # ============================

    return (player1, player2)


def phase1(var):
    player2 = var
    # ========== custom ==========
    player2.active_list.append(player2.card_list[5])
    player2.active_list.append(player2.card_list[2])
    # ============================
    return player2


def phase2(var):
    player1 = var[0]
    player2 = var[1]
    player1.active_list = []
    player2.active_list = []
    # ========== custom ==========
    player2.active_list.append(player2.card_list[3])
    player2.active_list.append(player2.card_list[1])
    # ============================
    return (player1, player2)

def get_common():
    # ========== custom ==========
    return Card('Red', 2)
    # ============================

if __name__ == '__main__':
    print("This File is not executable file. please run main.py.")