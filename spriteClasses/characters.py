import pygame


class Player(pygame.sprite.Sprite):

    PLAYER_SIZE = (50, 50)

    def __init__(self, color, pos):
        super(Player, self).__init__()

        self.image = pygame.image.load("assets/testpmnboy.png")
        self.image = pygame.transform.scale(self.image, self.PLAYER_SIZE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
