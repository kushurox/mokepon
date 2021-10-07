import pygame

from utils.attacks import Explosion, CrimsonBeam

clock = pygame.time.Clock()


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
    attacks = {}

    def __init__(self):
        super(Destroyer, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/blue_mokepon.png")
        self.rect = self.image.get_rect()
        self.attacks["Explosion"] = Explosion(dmg=self.atk, anim_time=3000)


class Byru(Mokepon):
    defense = 60
    atk = 40
    attacks = {}

    def __init__(self):
        super(Byru, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/red_mokepon.png")
        self.rect = self.image.get_rect()
        self.attacks["Crimson Beam"] = CrimsonBeam(dmg=self.atk, anim_time=1500)


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
