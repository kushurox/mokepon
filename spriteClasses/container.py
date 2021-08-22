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
        if args and not self.occupied:
            if self.rect.collidepoint(*args[0]):
                self.image.fill(HOVER_CONTAINER)
                self.groups()[0].current_tile = self
            else:
                self.image.fill(DEFAULT_CONTAINER)