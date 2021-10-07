from random import randint

import pygame

clock = pygame.time.Clock()


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Attack(pygame.sprite.Sprite):     # Inheriting from pygame.sprite.Sprite Class
    offset_x, offset_y = 0, 0
    name = None
    sound = None
    dmg = None
    anim_time = None
    dmg_ratio = None

    def __init__(self, dmg, anim_time):   # Constructor
        super(Attack, self).__init__()
        self.anim_time = anim_time
        self.dmg = self.dmg_ratio * dmg

    def animate(self, context, dt, x, y):
        pass

    def reset(self):
        self.offset_x = 0
        self.offset_y = 0

    def get_damage(self, defense):
        return (self.dmg - defense) - randint(5, 15)


class Explosion(Attack):
    dmg_ratio = 1.5

    def __init__(self, dmg, anim_time):
        super(Explosion, self).__init__(dmg, anim_time)
        self.image = rot_center(pygame.image.load("assets/battle_assets/missile.png"), 210)
        self.rect = self.image.get_rect()

    def animate(self, context, dt, x, y):
        self.offset_y += 100 * dt
        self.offset_x -= 50 * dt
        context.screen.blit(self.image, (x + self.offset_x, y + self.offset_y))


class CrimsonBeam(Attack):
    dmg_ratio = 1.8

    def __init__(self, dmg, anim_time):
        super(CrimsonBeam, self).__init__(dmg, anim_time)
        self.image = rot_center(pygame.image.load("assets/battle_assets/crimsonbeam.png"), -50)
        self.rect = self.image.get_rect()

    def animate(self, context, dt, x, y):
        self.offset_x += 100 * dt
        self.offset_y -= 50 * dt
        context.screen.blit(self.image, (x + self.offset_x, y + self.offset_y))
