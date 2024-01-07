import pygame
import os
import sys
from random import choice, randint

from man import AnimatedMan
from enemy import AnimatedEnemy
from background import Background
from let import Let
from bullet import Bullet

pygame.init()
size = width, height = 1000, 720
screen = pygame.display.set_mode(size)
new_color = None


def load_image(name, colorkey=None):
    global new_color
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    pixels = pygame.PixelArray(image)
    old_color = (3, 169, 244)
    new_color = choice(
        [(3, 169, 244), (192, 23, 0), (50, 50, 255), (232, 82, 190), (235, 128, 0), (50, 239, 1), (20, 20, 20),
         (255, 255, 0)])
    pixels.replace(old_color, new_color)
    del pixels

    if colorkey == 1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    elif colorkey == 0:
        image = image.convert_alpha()
    image = pygame.transform.scale(image, (440, 120))
    return image


def check_coords(r1, r2, x, y):
    k = 0
    for i in range(len(x)):
        if min([r2, y[i]]) + 250 > max([r2, y[i]]):
            if max([r1, x[i]]) > min([r1, x[i]]) + 270:
                k += 1
        else:
            k += 1
    if k == len(x):
        return True


if __name__ == '__main__':
    clock = pygame.time.Clock()
    fps = 60
    running = True

    bgs = pygame.sprite.Group()
    Background(bgs)

    lets = pygame.sprite.Group()
    x, y = [], []
    for i in range(100):
        r1, r2 = randint(180, 670), randint(122, 5000)
        if check_coords(r1, r2, x, y):
            x.append(r1)
            y.append(r2)
    for i1 in range(len(x)):
        Let(lets, x[i1], y[i1])

    men_run = pygame.sprite.Group()
    amogus_run = AnimatedMan(men_run, load_image('amogus_run.png', 1), 4, 1, 425, 560)

    enemies = pygame.sprite.Group()
    enemy = AnimatedEnemy(enemies, 6, 1, 0, -130)

    bullets = pygame.sprite.Group()

    while running:
        man_x, bul_y = amogus_run.get_coords()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet(bullets, man_x, bul_y, new_color)

        if len(lets) < 5:
            x, y = x[-3:-1], y[-3:-1]
            for i in range(100):
                r1, r2 = randint(180, 670), randint(130, 5000)
                if check_coords(r1, r2, x, y):
                    x.append(r1)
                    y.append(r2)
            for i in range(3, len(x)):
                Let(lets, x[i], y[i])
            enemy = AnimatedEnemy(enemies, 6, 1, man_x, -130)

        screen.fill((255, 255, 255))
        bgs.draw(screen)
        bgs.update()

        lets.draw(screen)
        lets.update(amogus_run, lets)

        men_run.draw(screen)
        men_run.update(event)

        enemies.draw(screen)
        enemies.update(man_x, bullets, enemies, amogus_run)

        bullets.draw(screen)
        bullets.update(bullets)

        clock.tick(fps)
        pygame.display.flip()
