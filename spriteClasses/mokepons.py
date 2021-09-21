import pygame
import random


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


class Destroyer(Mokepon):
    atk = 95
    defense = 40
    attacks = {"explosion": [atk*1.5, 3]}

    def __init__(self):
        super(Destroyer, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/blue_mokepon.png")
        self.rect = self.image.get_rect()

    def attack(self, mokepon: Mokepon, attack_choice: str):
        mokepon.hp -= (self.attacks[attack_choice][0] - self.defense + random.randint(5, 15))
        t = self.attacks[attack_choice][1]


class Byru(Mokepon):
    defense = 60
    atk = 70
    attacks = {"Crimson Beam": [atk * 1.5, 3], "nice": [1], "lol": [12]}

    def __init__(self):
        super(Byru, self).__init__()
        self.image = pygame.image.load("assets/battle_assets/red_mokepon.png")
        self.rect = self.image.get_rect()

    def attack(self, mokepon: Mokepon, attack_choice: str):
        mokepon.hp -= (self.attacks[attack_choice][0] - self.defense + random.randint(5, 15))
        t = self.attacks[attack_choice][1]



if __name__ == '__main__':
    d1, d2 = Destroyer(), Destroyer()



