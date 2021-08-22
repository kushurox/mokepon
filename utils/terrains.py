import pygame

DIR = "assets/surfaces"


class Terrain(pygame.sprite.Sprite):
    collision = False

    def __init__(self, name):
        super(Terrain, self).__init__()

        self.image = pygame.image.load(DIR + "/" + name)

        self.rect = self.image.get_rect()
