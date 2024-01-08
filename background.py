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


class Background(pygame.sprite.Sprite):
    image = load_image('BG.png')

    def __init__(self, group):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.y = -720

    def update(self):
        if self.rect.y >= 0:
            self.rect.y = -720
        self.rect = self.rect.move(0, 7)
