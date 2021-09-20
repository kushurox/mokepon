import pickle

import pandas
import pygame

from utils.color import RED
from utils.constants import default_sprite_res

DIR = "assets/surfaces"

ids = {
    'ghas.png': 0,
    'grass1.png': 1,
    'hill.png': 2,
    'hill4.png': 3,
    'hill5.png': 4,
    'hill6.png': 5,
    'hill8.png': 6,
    'hill7.png': 7,
    'hill2.png': 8,
    'hill3.png': 9,
    'path1.png': 10,
    'path2.png': 11,
    'pathend_d.png':12,
    'pathend_l.png':13,
    'pathend_r.png':14,
    'pathend_t.png':15,
    't_d.png':16,
    't_l.png':17,
    't_r.png':18,
    't_t.png':19,
    'crossroad.png':20,
    'elbow1.png':21,
    'elbow2.png':22,
    'elbow3.png':23,
    'elbow4.png':24,
    'stairs.png': 25,
    'haus_8.png' :26,
    'haus_9.png' :27,
    'haus_10.png' :28,
    'haus_11.png' :29,
    'haus_14.png' :30,
    'haus_15.png' :31,
    'haus_16.png' :32,
    'haus_17.png' :33,
    'haus_20.png':34,
    'haus_21.png':35,
    'haus_22.png':36,
    'haus_23.png':37,
    'haus_26.png':38,
    'haus_27.png':39,
    'door.png':   40,
    'haus_29.png':41
}


#door.png is door
#1, 3, 4, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,24,25,26,27,28, -1
collide_id = []

rev_ids = {-1: pygame.image.load(f"{DIR}/hill.png")}

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
    contains = []

    def __init__(self, s, block_id):
        super(GameTerrain, self).__init__(s)
        self.rect = self.get_rect()
        if block_id in collide_id:
            self.collide = True
        self.block_id = block_id
        self.blit(rev_ids[self.block_id], (0, 0))

    def add(self, item):
        item.rect.x = self.rect.x
        item.rect.y = self.rect.y
        self.contains.append(item)


class Terrains:
    terrains = []

    terrain_to_entity = {}

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


def load_map(map_name: str) -> Terrains:
    y = 0
    _map = Terrains()
    with open(map_name, "rb") as fp:
        df = pickle.load(fp)
    for row in df:
        x = 0
        for block in row:
            t = GameTerrain(default_sprite_res, block)
            t.rect.x = x
            t.rect.y = y
            x += 50
            _map.add(t)
        y += 50
    return _map


