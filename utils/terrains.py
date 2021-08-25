import pygame

from utils.color import RED
from utils.constants import default_sprite_res

DIR = "assets/surfaces"

ids = {
    'ghas.png': 0,
    'hill.png': 1,
    'grass1.png': 2,
    'hill2.png': 3,
    'hill3.png': 4,
    'path1.png': 5,
    'path2.png': 6,
    'stairs.png': 7
}

rev_ids = {}

for key, val in ids.items():
    rev_ids[val] = pygame.image.load(f"{DIR}/{key}")


class Terrain(pygame.sprite.Sprite):
    occupied = False

    block_id = 0

    def __init__(self, name):
        super(Terrain, self).__init__()
        self.selected_surf = pygame.Surface(default_sprite_res)
        self.selected_surf.fill(RED)
        self.block_id = ids[name]

        self.image = pygame.image.load(DIR + "/" + name).convert_alpha()
        self.original = self.image

        self.rect = self.image.get_rect()

    def update(self, *args, **kwargs) -> None:
        if not self.occupied and self.rect.collidepoint(args[0], args[1]):
            self.groups()[0].current_tile = self

            x, y = self.rect.x, self.rect.y
            self.image = self.selected_surf
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

        else:
            x, y = self.rect.x, self.rect.y
            self.image = self.original
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


class GameTerrain(pygame.Surface):
    collide = False

    def __init__(self, s, block_id, can_collide: bool):
        super(GameTerrain, self).__init__(s)
        self.rect = self.get_rect()
        self.collide = can_collide
        self.block_id = block_id
        self.blit(rev_ids[self.block_id], (0, 0))


class Terrains:
    terrains = []

    def add(self, terrain: GameTerrain):
        self.terrains.append(terrain)

    def remove(self, terrain: GameTerrain):
        self.terrains.remove(terrain)

    def get_terrain(self, x, y) -> GameTerrain:
        for terrain in self.terrains:
            if terrain.rect.collidepoint(x, y):
                return terrain

    def draw(self, surface):
        for tile in self.terrains:
            surface.blit(tile, (tile.rect.x, tile.rect.y))


def load_map():
    pass
