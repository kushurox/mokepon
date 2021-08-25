import pygame
# walk_left  = []
# walk_right = []
# walk_up    = []
# walk_down  = []
# idle       = [pygame.image.load()]
from utils.terrains import GameTerrain


class Player(pygame.sprite.Sprite):

    next_bob = 0.5

    status = False

    PLAYER_SIZE = (50, 50)
    bobs = {
        True: pygame.image.load("assets/char_animation/boy_idle/mpknboy1.png"),
        False: pygame.image.load("assets/char_animation/boy_idle/mpknboy2.png")
    }

    def __init__(self, color, current_tile: GameTerrain):
        super(Player, self).__init__()

        self.image = self.bobs[False]
        self.image = pygame.transform.scale(self.image, self.PLAYER_SIZE)

        self.current_tile = current_tile

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = current_tile.rect.x, current_tile.rect.y

    def update(self, *args, **kwargs) -> None:
        dt = args[0]
        self.next_bob -= dt
        if self.next_bob <= 0:
            self.image = self.bobs[self.status]
            self.status = not self.status
            self.next_bob = 0.5

    @staticmethod
    def target(terrain: GameTerrain):
        return not terrain.collide

    def up(self, t: GameTerrain):
        if self.target(t):
            self.rect.y -= 50

    def down(self, t: GameTerrain):
        if self.target(t):
            self.rect.y += 50

    def left(self, t: GameTerrain):
        if self.target(t):
            self.rect.x -= 50

    def right(self, t: GameTerrain):
        if self.target(t):
            self.rect.x += 50






