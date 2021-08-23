import pygame
from utils.color import DEFAULT_CONTAINER, HOVER_CONTAINER


class Air(pygame.sprite.Sprite):
    occupied = False

    def __init__(self, size, color, pos):
        super(Air, self).__init__()

        self.color = color

        self.image = pygame.Surface(size)

        self.image.fill(self.color)

        self.rect = self.image.get_rect()

        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self, *args):
        s = not self.occupied
        if args:
            if self.rect.collidepoint(*args[0]):
                self.groups()[0].current_tile = self

            if s and self.rect.collidepoint(*args[0]):
                self.image.fill(HOVER_CONTAINER)
            elif s:
                self.image.fill(DEFAULT_CONTAINER)

    def set_terrain(self, t):
        x, y = self.rect.x, self.rect.y
        self.image = t.original.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
