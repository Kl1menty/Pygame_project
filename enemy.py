import pygame
import os
import sys


def load_image(name, colorkey=None):
    global new_color
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
    image = pygame.transform.scale(image, (660, 130))
    return image


class AnimatedEnemy(pygame.sprite.Sprite):
    image = load_image('enemy.png')

    def __init__(self, group, columns, rows, x, y):
        super().__init__(group)
        self.a = 0
        self.frames = []
        self.cut_sheet(self.image, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, image, columns, rows):
        self.rect = pygame.Rect(0, 0, image.get_width() // columns,
                                image.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(image.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def collide(self):
        if self.rect.y == 440:
            return True
        return False

    def update(self, x, bullets, enemies, amogus_run):
        self.a += 1
        if self.a == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.a = 0
        self.rect = self.rect.move(0, 3)
        self.rect.x = x
        if pygame.sprite.spritecollideany(self, bullets):
            enemies.remove(self)
            pygame.mixer.music.load('data/shredder.mp3')
            pygame.mixer.music.play()
