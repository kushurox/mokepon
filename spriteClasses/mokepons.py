import pygame
import random

clock = pygame.time.Clock()


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Mokepon(pygame.sprite.Sprite):
    name = ""
    hp = 100
    defense = 30
    atk = 80
    agility = 30
    attacks = {}
    projectile = None
    sound_effect = None

    temp_time = 0

    def __init__(self):
        super(Mokepon, self).__init__()


# Attack structure (damage, delay, image)

class Destroyer(Mokepon):
    atk = 95
    defense = 40
    attacks = {"explosion": [atk * 1.5, 3000]}

    def __init__(self):
        super(Destroyer, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/blue_mokepon.png")
        self.rect = self.image.get_rect()
        img = pygame.image.load("assets/battle_assets/missile.png")
        img = rot_center(img, 210)
        self.attacks['explosion'].append(img)


class Byru(Mokepon):
    defense = 60
    atk = 40
    attacks = {"Crimson Beam": [atk * 1.5, 1000]}

    def __init__(self):
        super(Byru, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/red_mokepon.png")
        self.rect = self.image.get_rect()
        img = pygame.image.load("assets/battle_assets/crimsonbeam.png")
        img = rot_center(img, -50)
        self.attacks["Crimson Beam"].append(img)

class Orb(Mokepon):
    atk = 100
    attacks = {"Anurism": [atk * 1.5, 3], "nice": [1], "lol": [12]}

    def __init__(self):
        super(Orb, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/green_mokepon.png")
        self.rect = self.image.get_rect()

# TODO Change attack architecture


if __name__ == '__main__':
    d1, d2 = Destroyer(), Destroyer()
    d1.attack(d2, "explosion")
