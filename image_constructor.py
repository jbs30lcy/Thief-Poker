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

# =========== 1 ===========
pg.draw.circle(Card, Red, (200, 300), 40)

# =========== 2 ===========
# pg.draw.circle(Card, Red, (200, 150), 30)
# pg.draw.circle(Card, Red, (200, 450), 30)

# =========== 3 ===========
# pg.draw.circle(Card, Red, (200, 150), 30)
# pg.draw.circle(Card, Red, (80, 400), 30)
# pg.draw.circle(Card, Red, (320, 400), 30)

# =========== 4 ===========
# pg.draw.circle(Card, Red, (80, 150), 25)
# pg.draw.circle(Card, Red, (320, 150), 25)
# pg.draw.circle(Card, Red, (80, 450), 25)
# pg.draw.circle(Card, Red, (320, 450), 25)

# =========== 5 ===========
# pg.draw.circle(Card, Red, (80, 150), 25)
# pg.draw.circle(Card, Red, (320, 150), 25)
# pg.draw.circle(Card, Red, (80, 450), 25)
# pg.draw.circle(Card, Red, (320, 450), 25)
# pg.draw.circle(Card, Red, (200, 300), 25)

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
# pg.image.save(Card, img_dir_path + 'Red_1.png')



while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
    
    screen.blit(Card, (0, 0))

    clock.tick(60)
    pg.display.update()