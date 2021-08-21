import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, color, size, pos):
        super(Player, self).__init__()

        self.image = pygame.image.load("assets/pkmn boy.png")
        # self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
