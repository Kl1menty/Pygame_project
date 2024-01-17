import sys
import pygame


class AnimatedMan(pygame.sprite.Sprite):

    def __init__(self, group, image, columns, rows, x, y):
        super().__init__(group)
        self.a = 0
        self.image = image
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

    def get_coords(self):
        return self.rect.x, self.rect.y

    def collide(self, lets):
        for i in lets:
            if pygame.sprite.collide_mask(self, i):
                return True
        return False

    def update(self, *args):
        self.a += 1
        if self.a == 5:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.a = 0

        if args:
            if args[0].type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_RIGHT] or \
                    pygame.key.get_pressed()[pygame.K_d]:
                if self.rect.x <= 713:
                    self.rect = self.rect.move(10, 0)
            elif args[0].type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_LEFT] or \
                    pygame.key.get_pressed()[pygame.K_a]:
                if self.rect.x >= 170:
                    self.rect = self.rect.move(-10, 0)
            if args[0].type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_UP]:
                pass
