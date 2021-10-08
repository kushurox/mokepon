import pygame

from utils.attacks import Explosion, CrimsonBeam, Harden, Cut

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
        self.attacks["Explosion"] = Explosion(self, dmg=self.atk, anim_time=3000)

    def reset(self):
        self.defense = 60
        self.atk = 40
        self.hp = 100


class Byru(Mokepon):
    defense = 60
    atk = 40
    hp = 120
    attacks = {}

    def __init__(self):
        super(Byru, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/red_mokepon.png")
        self.rect = self.image.get_rect()
        self.attacks["Crimson Beam"] = CrimsonBeam(self, dmg=self.atk, anim_time=1500)
        self.attacks["Harden"] = Harden(self, dmg=0, anim_time=2000)

    def reset(self):
        self.defense = 60
        self.atk = 40
        self.hp = 120


class Orb(Mokepon):
    atk = 100
    attacks = {}

    def __init__(self):
        super(Orb, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/green_mokepon.png")
        self.rect = self.image.get_rect()
        self.attacks["Cut"] = Cut(self, dmg=self.atk, anim_time=2000)

    def reset(self):
        self.hp = 100
        self.defense = 60
        self.atk = 40


# TODO Change attack architecture


if __name__ == '__main__':
    d1, d2 = Destroyer(), Destroyer()
    d1.attack(d2, "explosion")
