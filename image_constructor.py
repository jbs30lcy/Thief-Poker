# image_constructor.py : img 폴더의 각 카드 이미지를 생성했던 파일. 사용하지 않는 파일이다

import pygame as pg
from pygame.locals import *
from obj import *
import sys
import pygame.gfxdraw as pgg
pg.init()
WIDTH = 400
HEIGHT = 600
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Image Constructor")
clock = pg.time.Clock()

tick = 0
Card = pg.Surface((WIDTH, HEIGHT))
Card.fill(Grey2)

# =========== 이 3개만 건드릴 것! ==========
check_num = 7
check_color = Yellow
check_name = 'Yellow'

# =========== 1 ===========
if check_num == 1:
    pg.draw.circle(Card, check_color, (200, 300), 40)

# =========== 2 ===========
elif check_num == 2:
    pg.draw.circle(Card, check_color, (200, 150), 30)
    pg.draw.circle(Card, check_color, (200, 450), 30)

# =========== 3 ===========
elif check_num == 3:
    pg.draw.circle(Card, check_color, (200, 150), 30)
    pg.draw.circle(Card, check_color, (80, 400), 30)
    pg.draw.circle(Card, check_color, (320, 400), 30)

# =========== 4 ===========
elif check_num == 4:
    pg.draw.circle(Card, check_color, (80, 150), 25)
    pg.draw.circle(Card, check_color, (320, 150), 25)
    pg.draw.circle(Card, check_color, (80, 450), 25)
    pg.draw.circle(Card, check_color, (320, 450), 25)

# =========== 5 ===========
elif check_num == 5:
    pg.draw.circle(Card, check_color, (80, 150), 25)
    pg.draw.circle(Card, check_color, (320, 150), 25)
    pg.draw.circle(Card, check_color, (80, 450), 25)
    pg.draw.circle(Card, check_color, (320, 450), 25)
    pg.draw.circle(Card, check_color, (200, 300), 25)

elif check_num == 6:
    pg.draw.circle(Card, check_color, (70, 200), 25)
    pg.draw.circle(Card, check_color, (70, 400), 25)
    pg.draw.circle(Card, check_color, (200, 500), 25)
    pg.draw.circle(Card, check_color, (330, 400), 25)
    pg.draw.circle(Card, check_color, (330, 200), 25)
    pg.draw.circle(Card, check_color, (200, 100), 25)

# =========== 7 ===========
elif check_num == 7:
    pg.draw.circle(Card, check_color, (70, 200), 25)
    pg.draw.circle(Card, check_color, (70, 400), 25)
    pg.draw.circle(Card, check_color, (200, 500), 25)
    pg.draw.circle(Card, check_color, (330, 400), 25)
    pg.draw.circle(Card, check_color, (330, 200), 25)
    pg.draw.circle(Card, check_color, (200, 100), 25)
    pg.draw.circle(Card, check_color, (200, 300), 25)

# =========== Black ===========
# F = pg.font.SysFont('Arialrounded', 84)
# pg.draw.circle(Card, Black, (200, 300), 60)
# pg.draw.circle(Card, White, (200, 300), 20)
# for lx in range(40, 170, 2):
#     pgg.bezier(Card, [(170, 250), (150, 300), (lx, 300)], 2, Black)
#     pgg.bezier(Card, [(170, 350), (150, 300), (lx, 300)], 2, Black)
#     pgg.bezier(Card, [(230, 250), (250, 300), (400 - lx, 300)], 2, Black)
#     pgg.bezier(Card, [(230, 350), (250, 300), (400 - lx, 300)], 2, Black)
# text = F.render("Joker", True, Black)
# print(text.get_rect())
# Card.blit(text, (85, 80))

# ============ saving file ============
pg.image.save(Card, img_dir_path + f'{check_name}_{check_num}.png')


# ============ 하단은 폐기 =============
# Cardr = pg.Surface((WIDTH, HEIGHT))
# Cardy = pg.Surface((WIDTH, HEIGHT))
# Cardb = pg.Surface((WIDTH, HEIGHT))
# Cardg = pg.Surface((WIDTH, HEIGHT))
# Cardr.fill(Grey2)
# Cardy.fill(Grey2)
# Cardb.fill(Grey2)
# Cardg.fill(Grey2)

# for color in (Red, Yellow, Blue, Green):
#     if color == Red:
#         card = Cardr
#         name = 'Red'
#     if color == Yellow:
#         card = Cardy
#         name = 'Yellow'
#     if color == Blue:
#         card = Cardb
#         name = 'Blue'
#     if color == Green:
#         card = Cardg
# #     pg.draw.circle(card, color, (70, 200), 25)
# #     pg.draw.circle(card, color, (70, 400), 25)
# #     pg.draw.circle(card, color, (200, 500), 25)
# #     pg.draw.circle(card, color, (330, 400), 25)
# #     pg.draw.circle(card, color, (330, 200), 25)
# #     pg.draw.circle(card, color, (200, 100), 25)
# #     pg.draw.circle(card, color, (200, 300), 25)

#     pg.image.save(card, img_dir_path + f'{name}_7.png')

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    
    screen.blit(Card, (0, 0))

    clock.tick(60)
    pg.display.update()