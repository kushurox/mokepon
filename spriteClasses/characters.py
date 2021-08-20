import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, color, size):
        super(Player, self).__init__()

        self.image = pygame.Surface(size)
        self.image.fill(color)

        self.rect = self.image.get_rect()
