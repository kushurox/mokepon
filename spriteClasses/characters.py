import pygame

from utils.camera import GameCamera
from utils.color import RED
from utils.constants import window_size
from utils.terrains import GameTerrain, Terrains


class Player(pygame.sprite.Sprite):
    next_bob = 300

    gender = None

    movementX = {
        pygame.K_a: -48,
        pygame.K_d: 52,
        pygame.K_w: 0,
        pygame.K_s: 0
    }

    area = None

    moving = False

    tt = None

    status = False

    PLAYER_SIZE = (50, 50)

    bobs = {}

    def __init__(self, color: tuple, whole_area: Terrains, gender: int, camera: GameCamera):
        super(Player, self).__init__()

        self.camera = camera

        self.gender = gender
        if gender == 1:  # male
            self.bobs[True] = pygame.image.load("assets/char_animation/boy_idle/mpknboy1.png")
            self.bobs[False] = pygame.image.load("assets/char_animation/boy_idle/mpknboy2.png")
            self.character_sprite1 = {
                pygame.K_a: pygame.image.load("assets/char_animation/boy_move/boyl1.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/boy_move/boyr1.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/boy_move/boyb1.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/boy_move/boyf1.png"),
                -1: pygame.image.load("assets/char_animation/boy_idle/mpknboy1.png")
            }
            self.character_sprite2 = {
                pygame.K_a: pygame.image.load("assets/char_animation/boy_move/boyl2.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/boy_move/boyr2.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/boy_move/boyb2.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/boy_move/boyf2.png"),
                -1: pygame.image.load("assets/char_animation/boy_idle/mpknboy2.png")
            }
        elif gender == 0:
            self.bobs[True] = pygame.image.load("assets/char_animation/girl_idle/mpkngirl1.png")
            self.bobs[False] = pygame.image.load("assets/char_animation/girl_idle/mpkngirl2.png")
            self.character_sprite1 = {
                pygame.K_a: pygame.image.load("assets/char_animation/girl_move/girll1.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/girl_move/girlr1.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/girl_move/girlb1.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/girl_move/girlf1.png"),
                -1: pygame.image.load("assets/char_animation/girl_idle/mpkngirl1.png")
            }
            self.character_sprite2 = {
                pygame.K_a: pygame.image.load("assets/char_animation/girl_move/girll2.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/girl_move/girlr2.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/girl_move/girlb2.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/girl_move/girlf2.png"),
                -1: pygame.image.load("assets/char_animation/girl_idle/mpkngirl2.png")
            }

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
            self.next_bob = 300

    def move(self, pmx, pmy, pkx, pky, movementX, movementY, wt):

        if pmx and not pmy:
            x = movementX[pkx]
            x *= wt
            dx = self.rect.x + x
            if x < 0:
                contact_tile = self.area.get_terrain(dx, self.rect.y + 25)
            else:
                contact_tile = self.area.get_terrain(dx + 50, self.rect.y + 25)

            if self.target(contact_tile):
                self.rect.x = dx
                self.camera.begin_x = self.rect.x - 300

        if pmy and not pmx:
            y = movementY[pky]
            y *= wt
            dy = self.rect.y + y
            sign = dy / -dy
            if y < 0:
                contact_tile = self.area.get_terrain(self.rect.x + 25, dy)
            else:
                contact_tile = self.area.get_terrain(self.rect.x + 25, dy + 50)

            if self.target(contact_tile):
                self.rect.y = dy
                self.camera.begin_y = self.rect.y - 300

        self.current_tile = self.area.get_terrain(self.rect.x+25 + self.camera.x_offset, self.rect.y+25 + self.camera.y_offset)

    @staticmethod
    def target(terrain: GameTerrain):
        if terrain:
            return not terrain.collide

    def get_move(self, key):
        if key in self.movementX:
            return self.current_tile
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class NPC(pygame.sprite.Sprite):
    def __init__(self, pos, area: Terrains):
        super(NPC, self).__init__()
        self.area = area
        self.current_tile = area.get_terrain(*pos)
        self.current_tile.collide = True
        self.image = pygame.image.load("assets/char_animation/girl_idle/mpkngirl1.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
