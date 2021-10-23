import random
from random import randint

import pygame

from utils.color import RED, GREEN
from utils.constants import PLAYER_MOKEPON_POSITION, MOKEPON_SPRITE_SIZE, ENEMY_MOKEPON_POSITION

clock = pygame.time.Clock()


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Attack(pygame.sprite.Sprite):  # Inheriting from pygame.sprite.Sprite Class
    offset_x, offset_y = 0, 0
    name = None
    sound = None
    dmg = None
    anim_time = None
    dmg_ratio = None

    def __init__(self, mokepon, dmg, anim_time):  # Constructor
        super(Attack, self).__init__()
        self.anim_time = anim_time
        self.dmg = self.dmg_ratio * dmg
        self.mokepon = mokepon

    def animate(self, context, dt, x, y):
        pass

    def reset(self):
        self.offset_x = 0
        self.offset_y = 0

    def get_damage(self, defense):
        dmg = (self.dmg - defense) + randint(5, 15)
        return dmg if self.dmg-defense > 0 else 5

    def status(self, context, changed, enemy):
        context.dialogue([f"{self.mokepon.__class__.__name__} has done {changed} dmg!"])


class Explosion(Attack):
    dmg_ratio = 1.5

    def __init__(self, mokepon, dmg, anim_time):
        super(Explosion, self).__init__(mokepon, dmg, anim_time)
        self.image = rot_center(pygame.image.load("assets/battle_assets/missile.png"), 210)
        self.rect = self.image.get_rect()

    def animate(self, context, dt, x, y):
        self.offset_y += 100 * dt
        self.offset_x -= 50 * dt
        context.screen.blit(self.image, (x + self.offset_x, y + self.offset_y))


class CrimsonBeam(Attack):
    dmg_ratio = 1.8

    def __init__(self, mokepon, dmg, anim_time):
        super(CrimsonBeam, self).__init__(mokepon, dmg, anim_time)
        self.image = rot_center(pygame.image.load("assets/battle_assets/crimsonbeam.png"), -50)
        self.rect = self.image.get_rect()

    def animate(self, context, dt, x, y):
        self.offset_x += 100 * dt
        self.offset_y -= 50 * dt
        context.screen.blit(self.image, (x + self.offset_x, y + self.offset_y))  # Showing the drawing on the screen

    def get_damage(self, defense):
        dmg = (self.dmg - defense) + randint(5, 17)
        return dmg if self.dmg-defense > 0 else 5


class Harden(Attack):
    dmg_ratio = 0

    def __init__(self, mokepon, dmg, anim_time):
        super(Harden, self).__init__(mokepon, dmg, anim_time)

    def animate(self, context, dt, x, y):
        self.offset_x += 60 * dt
        show_pos = (PLAYER_MOKEPON_POSITION[0] + MOKEPON_SPRITE_SIZE//2,
                    PLAYER_MOKEPON_POSITION[1] + MOKEPON_SPRITE_SIZE//2)
        pygame.draw.circle(context.screen, RED, show_pos, self.offset_x)

    def status(self, context, changed, enemy):
        context.dialogue([f"{self.mokepon.__class__.__name__}'s defense has increased by 30!"])
        self.mokepon.defense += 30

    def get_damage(self, defense):
        return 0


class Cut(Attack):
    dmg_ratio = 1

    def animate(self, context, dt, x, y):
        self.offset_y += 100 * dt
        pygame.draw.line(context.screen, RED,
                         [ENEMY_MOKEPON_POSITION[0] + 100, ENEMY_MOKEPON_POSITION[1]+100],
                         (PLAYER_MOKEPON_POSITION[0], PLAYER_MOKEPON_POSITION[1] + self.offset_y))

    def status(self, context, changed, enemy):
        super(Cut, self).status(context, changed, enemy)
        context.dialogue([f"{enemy.__class__.__name__} has lost 45 defense!"])
        enemy.defense -= 45

    #def get_damage(self, defense):
     #   return random.randint(20,50)




