import pygame
import os
import sys
from background import Background
from man import AnimatedSprite

pygame.init()
size = width, height = 1000, 720
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == 1:
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    elif colorkey == 0:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    clock = pygame.time.Clock()
    fps = 60
    running = True

    bgs = pygame.sprite.Group()
    Background(bgs)

    men = pygame.sprite.Group()
    dragon = AnimatedSprite(men, load_image("amogus.png", 1), 4, 1, 425, 500)
    a = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        bgs.draw(screen)
        bgs.update()
        men.draw(screen)
        a += 1
        if a == 3:
            men.update()
            a = 0

        clock.tick(fps)
        pygame.display.flip()
