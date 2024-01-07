import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey == 1:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    elif colorkey == 0:
        image = image.convert_alpha()
    return image


class Bullet(pygame.sprite.Sprite):
    image = load_image('bullet.png')

    def __init__(self, group, x, y, color):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = x + 110 / 2 - 9 // 2
        self.rect.y = y - 30
        self.change_color(color)

    def change_color(self, new_color):
        pixels = pygame.PixelArray(self.image)
        old_color = (255, 193, 7)
        pixels.replace(old_color, new_color)
        del pixels

    def update(self, bullets):
        self.rect = self.rect.move(0, -10)
        if self.rect.y == 0:
            bullets.remove(self)