import pygame
# walk_left  = []
# walk_right = []
# walk_up    = []
# walk_down  = []
# idle       = [pygame.image.load()]
from utils.terrains import GameTerrain


class Player(pygame.sprite.Sprite):
    next_bob = 500

    is_moving = False
    destX = 0
    destY = 0

    movementX = {
        pygame.K_a: -48,
        pygame.K_d: 52,
        pygame.K_w: 0,
        pygame.K_s: 0
    }
    movementY = {
        pygame.K_w: -48,
        pygame.K_s: 52,
        pygame.K_a: 0,
        pygame.K_d: 0
    }

    ms = 500

    tt = None

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
            self.next_bob = 500

        if self.is_moving:
            self.ms -= dt
            if not self.target(self.tt):
                self.is_moving = False
                self.ms = 500

            if 0 < self.ms <= 250:
                self.destX -= self.destX // 2
                self.destY -= self.destY // 2
                self.rect.x += self.destX
                self.rect.y += self.destY

            # s = self.destX/(self.ms/1000)

            elif self.ms <= 0:
                self.rect.x = self.tt.rect.x
                self.rect.y = self.tt.rect.y
                self.current_tile = self.tt
                self.ms = 500
                self.destX = 0
                self.destY = 0
                self.is_moving = False

    @staticmethod
    def target(terrain: GameTerrain):
        return not terrain.collide

    def move(self, t: GameTerrain):
        self.is_moving = True
        self.tt = t
        self.destX = self.tt.rect.x - self.rect.x
        self.destY = self.tt.rect.y - self.rect.y

    def get_move(self, key):
        if key in self.movementX:
            return self.current_tile.rect.x + self.movementX[key], self.current_tile.rect.y + self.movementY[key]
        return False
