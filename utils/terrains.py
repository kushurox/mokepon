import pygame

DIR = "assets/surfaces"

ids = {
    'ghas.png': 0,
    'hill.png': 1
}


class Terrain(pygame.sprite.Sprite):
    collision = False
    occupied = False

    block_id = 0

    def __init__(self, name):
        super(Terrain, self).__init__()
        self.selected_surf = pygame.Surface([50, 50])
        self.selected_surf.fill((255, 0, 0))

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




