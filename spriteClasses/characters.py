import pygame

from utils.constants import window_size
from utils.terrains import GameTerrain, Terrains


class Player(pygame.sprite.Sprite):
    next_bob = 500

    movementX = {
        pygame.K_a: -48,
        pygame.K_d: 52,
        pygame.K_w: 0,
        pygame.K_s: 0
    }

    area = None

    tt = None

    status = False

    PLAYER_SIZE = (50, 50)
    bobs = {
        True: pygame.image.load("assets/char_animation/girl_idle/mpkngirl1.png"),
        False: pygame.image.load("assets/char_animation/girl_idle/mpkngirl2.png")
    }

    def __init__(self, color, whole_area: Terrains):
        super(Player, self).__init__()

        self.image = self.bobs[False]
        self.image = pygame.transform.scale(self.image, self.PLAYER_SIZE)

        self.area = whole_area

        self.current_tile = whole_area.get_terrain(window_size[0] // 2, window_size[1] // 2)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.current_tile.rect.x, self.current_tile.rect.y

    def update(self, *args, **kwargs) -> None:
        dt = args[0]
        self.next_bob -= dt
        if self.next_bob <= 0:
            self.image = self.bobs[self.status]
            self.status = not self.status
            self.next_bob = 500

    def move(self, pmx, pmy, pkx, pky, movementX, movementY, wt):

        if pmx:
            x = movementX[pkx]
            x *= wt
            dx = self.rect.x + x
            if x < 0:
                contact_tile = self.area.get_terrain(dx, self.rect.y+25)
            else:
                contact_tile = self.area.get_terrain(dx + 50, self.rect.y+25)

            if self.target(contact_tile):
                self.rect.x = dx

        if pmy:
            y = movementY[pky]
            y *= wt
            dy = self.rect.y + y
            sign = dy / -dy
            if y < 0:
                contact_tile = self.area.get_terrain(self.rect.x+25, dy)
            else:
                contact_tile = self.area.get_terrain(self.rect.x+25, dy+50)

            if self.target(contact_tile):
                self.rect.y = dy

        self.current_tile = self.area.get_terrain(self.rect.x, self.rect.y)

    @staticmethod
    def target(terrain: GameTerrain):
        return not terrain.collide

    def get_move(self, key):
        if key in self.movementX:
            return self.current_tile
        return False
