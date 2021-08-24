import pygame
walk_left  = []
walk_right = []
walk_up    = []
walk_down  = []
idle       = [pygame.image.load()]

class Player(pygame.sprite.Sprite):

    next_bob = 1

    status = False

    PLAYER_SIZE = (50, 50)
    bobs = {
        True: pygame.image.load("assets/mkpngirl.gif"),
        False: pygame.image.load("assets/testpmnboy.png")
    }

    def __init__(self, color, pos):
        super(Player, self).__init__()

        self.image = self.bobs[False]
        self.image = pygame.transform.scale(self.image, self.PLAYER_SIZE)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

    def update(self, *args, **kwargs) -> None:
        dt = args[0]
        self.next_bob -= dt
        if self.next_bob <= 0:
            self.image = self.bobs[self.status]
            self.status = not self.status
            self.next_bob = 1





