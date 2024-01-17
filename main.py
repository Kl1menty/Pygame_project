import pygame
import os
import sys
from random import choice, randint
import _datetime as dt

from man import AnimatedMan
from enemy import AnimatedEnemy
from background import Background
from let import Let
from bullet import Bullet

pygame.init()
width, height = 1000, 720
screen = pygame.display.set_mode((width, height))
new_color = None
st_sc = True
ov_sc = False
transparency = 255
k = 5
pygame.mixer.init()
play_music = False
time_start = time_end = None
result = '00:00'
enemy = None


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
    new_color = (255, 0, 0)
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
        if min([r2, y[i]]) + 270 > max([r2, y[i]]):
            if max([r1, x[i]]) > min([r1, x[i]]) + 270:
                k += 1
        else:
            k += 1
    if k == len(x):
        return True


def start_screen():
    global transparency, k
    image = pygame.image.load('data/screensaver.jpg')
    screen.blit(image, (0, 0))

    intro_text = "нажмите  чтобы начать"
    font = pygame.font.Font(None, 28)
    string_rendered = font.render(intro_text, 1, (255, 255, 255))
    string_rendered.set_alpha(transparency)
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 37
    intro_rect.y = 670
    screen.blit(string_rendered, intro_rect)
    if transparency == 255:
        k = -5
    elif transparency == 0:
        k = 5
    transparency += k


def over_screen():
    image = pygame.image.load('data/game_over.png')
    screen.blit(image, (0, 0))

    text = f"Лучший результат: {best_result}"
    font = pygame.font.Font(None, 28)
    string_rendered = font.render(text, 1, (0, 0, 0))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = 370
    intro_rect.y = 175
    screen.blit(string_rendered, intro_rect)


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

    bullets = pygame.sprite.Group()

    while running:
        with open('data/best_result.txt', 'r') as br:
            best_result = br.readline()
            if result > best_result:
                f = open("data/best_result.txt", 'w')
                f.write(result)
                f.close()
        if st_sc:
            start_screen()
            if not play_music:
                pygame.mixer.music.load('data/game_start_or_fale.mp3')
                pygame.mixer.music.play()
                play_music = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    st_sc = False
                    pygame.mixer.music.stop()
                    play_music = False
                    time_start = dt.datetime.now()
            clock.tick(fps)
            pygame.display.flip()

        elif ov_sc:
            over_screen()
            if not play_music:
                pygame.mixer.music.load('data/game_start_or_fale.mp3')
                pygame.mixer.music.play()
                play_music = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(653, 213, 160, 160).collidepoint(event.pos):
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(227, 227, 135, 133).collidepoint(event.pos) \
                        or event.type == pygame.KEYDOWN:
                    time_start = dt.datetime.now()
                    ov_sc = False
                    pygame.mixer.music.stop()
                    play_music = False
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
                    bullets = pygame.sprite.Group()

            clock.tick(fps)
            pygame.display.flip()

        else:
            man_x, bul_y = amogus_run.get_coords()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('data/piu.mp3')
                    pygame.mixer.music.play()
                    bullet = Bullet(bullets, man_x, bul_y, new_color)

            if len(lets) == 5:
                for _ in range(len(x) - 5):
                    del x[0]
                    del y[0]
                for i in range(50):
                    r1, r2 = randint(180, 670), randint(130, 5000)
                    if check_coords(r1, r2, x, y):
                        x.append(r1)
                        y.append(r2)
                        Let(lets, r1, r2)

                enemy = AnimatedEnemy(enemies, 6, 1, man_x, -130)

            screen.fill((255, 255, 255))
            bgs.draw(screen)
            bgs.update()

            text = str(dt.datetime.now() - time_start)[2:9]
            font = pygame.font.Font(None, 36)
            string_rendered = font.render(text, 1, (255, 0, 0))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 860
            intro_rect.y = 40
            screen.blit(string_rendered, intro_rect)

            lets.draw(screen)
            lets.update(lets)

            men_run.draw(screen)
            men_run.update(event)
            if amogus_run.collide(lets):
                ov_sc = True
                time_end = dt.datetime.now()
                result = str(time_end - time_start)
                result = result[2:9]

            enemies.draw(screen)
            enemies.update(man_x, bullets, enemies, amogus_run)
            if enemy and enemy.collide():
                ov_sc = True
                time_end = dt.datetime.now()
                result = str(time_end - time_start)
                result = result[2:9]

            bullets.draw(screen)
            bullets.update(bullets)

            clock.tick(fps)
            pygame.display.flip()
