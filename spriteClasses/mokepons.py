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


class Destroyer(Mokepon):
    atk = 95
    defense = 40
    attacks = {"explosion": [atk*1.5, 3]}

    def attack(self, mokepon: Mokepon, attack_choice: str):
        mokepon.hp -= (self.attacks[attack_choice][0] - self.defense + random.randint(5, 15))
        t = self.attacks[attack_choice][1]


class Byru(Mokepon):
    defense = 60
    atk = 70
    attacks = {"Crimson Beam": [atk * 1.5, 3]}

    def attack(self, mokepon: Mokepon, attack_choice: str):
        mokepon.hp -= (self.attacks[attack_choice][0] - self.defense + random.randint(5, 15))
        t = self.attacks[attack_choice][1]


if __name__ == '__main__':
    d1, d2 = Destroyer(), Destroyer()



