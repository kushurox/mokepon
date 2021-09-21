import pygame
import random


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

    def __init__(self):
        super(Mokepon, self).__init__()

    def attack(self, mokepon, attack_choice: str):
        mokepon.hp -= (self.attacks[attack_choice][0] - self.defense + random.randint(5, 15))
        t = self.attacks[attack_choice][1]


# Attack structure (damage, delay, image)

class Destroyer(Mokepon):
    atk = 95
    defense = 40
    attacks = {"explosion": [atk * 1.5, 3]}

    def __init__(self):
        super(Destroyer, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/blue_mokepon.png")
        self.rect = self.image.get_rect()


class Byru(Mokepon):
    defense = 60
    atk = 70
    attacks = {"Crimson Beam": [atk * 1.5, 3]}

    def __init__(self):
        super(Byru, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/red_mokepon.png")
        self.rect = self.image.get_rect()
        img = pygame.image.load("assets/battle_assets/crimsonbeam.png")
        img = rot_center(img, -50)
        self.attacks["Crimson Beam"].append(img)


if __name__ == '__main__':
    d1, d2 = Destroyer(), Destroyer()
