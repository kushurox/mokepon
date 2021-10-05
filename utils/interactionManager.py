import random

import pygame
from cmath import sqrt
from utils.color import BLUE, GREY, RED, YELLOW, BLACK, WHITE

clock = pygame.time.Clock()


def dist(p, q):
    return sqrt((p[0] + q[0]) ** 2 + (p[1] - q[1]) ** 2).real


class InteractionManager:
    interaction = None
    args = []
    event = None

    def __init__(self, screen):
        self.screen = screen

    def set_interaction(self, interaction, *args):
        self.interaction = interaction
        self.args = args

    def update(self):
        if self.interaction:
            res = self.interaction(self, self.event, self.screen, *self.args)
            return res

        return False


class AttackUI(pygame.Surface):
    name = None
    rect = None
    atk_name = None

    def __init__(self, size, name):
        super(AttackUI, self).__init__(size)
        self.rect = self.get_rect()
        self.atk_name = name


class Battle:
    battle = True
    bg = pygame.image.load("assets/battle_assets/battle.png")
    HUD = pygame.Surface([650, 150])
    turn = 0
    tu1 = 1000
    u1 = 2
    u2 = -2
    battle_font = pygame.font.Font("assets/fonts/VPPixel-Simplified.otf", 24)
    anim_time = 0
    atk_choice = None

    def __init__(self, screen, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.mokepon1 = p1.mokepon
        self.mokepon2 = p2.mokepon

        self.attacks1 = []
        self.fonts = {}
        s, h = 0, 500
        for key in self.mokepon1.attacks:
            a = AttackUI([315, 65], key)
            a.fill((100, 100, 100, 50))
            a.rect.x = s
            a.rect.y = h
            s += 325
            if s == 650:
                s = 0
                h += 75
            if h == 650:
                h = 500

            self.attacks1.append(a)
            a.name = self.battle_font.render(key, False, BLUE)

        self.screen = screen

        self.HUD.fill(GREY)

        self.start_battle()

    def attack(self, attack_choice: str):
        self.mokepon2.hp -= ((self.mokepon1.attacks[attack_choice][0] - self.mokepon2.defense) + random.randint(5, 15))
        x, y = 175, 50
        while self.anim_time > 0:
            dt = clock.tick(30)
            e = dt/1000
            y -= 20 * e
            x += 60 * e
            self.anim_time -= dt
            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.mokepon1.attacks[attack_choice][2], (x, y))
            self.screen.blit(self.mokepon1.image, (50, 300 + self.u1))
            self.screen.blit(self.mokepon2.image, (400, 70 + self.u2))

            pygame.display.flip()

        self.dialogue(['hi', 'sup', 'kushurox'], pygame.image.load("assets/misc/koshugun.png"))
        self.turn = 0  # Change this to 2 later, 0 is for my own turn

    def dialogue(self, d: list, player=None):
        self.screen.blit(self.bg, (0, 0))
        if not player:
            self.screen.blit(self.mokepon1.image, (50, 300 + self.u1))
            self.screen.blit(self.mokepon2.image, (400, 70 + self.u2))
        else:
            self.screen.blit(player, (200, 400)) #  Dialogue Player Position
        d.append('')
        index = 0
        cd = d[index]
        fnt = self.battle_font.render(cd, False, WHITE)
        while index < len(d)-1:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    index += 1
                    cd = d[index]
                    fnt = self.battle_font.render(cd, False, WHITE)

            self.screen.blit(self.HUD, (0, 500))
            self.HUD.fill(GREY)
            self.HUD.blit(fnt, (30, 30))
            pygame.display.flip()


    def start_battle(self):
        while self.battle:
            dt = clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.battle = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    for atk in self.attacks1:
                        if not self.turn and atk.rect.collidepoint(x, y):
                            self.turn = 1
                            self.atk_choice = atk.atk_name
                            self.anim_time = self.mokepon1.attacks[atk.atk_name][1]
            self.screen.blit(self.bg, (0, 0))

            self.screen.blit(self.mokepon1.image, (50, 300 + self.u1))
            self.screen.blit(self.mokepon2.image, (400, 70 + self.u2))
            hp1 = pygame.draw.rect(self.screen, BLUE, (0, 0, 300, 26), 13, 8)
            hp2 = pygame.draw.rect(self.screen, RED, (350, 0, 650, 26), 13, 8)

            self.tu1 -= dt
            if self.tu1 <= 0:
                self.u1 = -self.u1
                self.u2 = -self.u2
                self.tu1 = 1000

            self.screen.blit(self.HUD, (0, 500))
            if not self.turn:  # TODO: ADD DIALOGUE MANAGER
                s = 0
                h = 0
                mx, my = pygame.mouse.get_pos()
                for atk in self.attacks1:
                    if atk.rect.collidepoint(mx, my):
                        atk.fill(YELLOW)
                    else:
                        atk.fill((100, 100, 100, 50))
                    self.HUD.blit(atk, (5 + s, 5 + h))
                    self.HUD.blit(atk.name, (20 + s, 15 + h))

                    s += 325
                    if s == 650:
                        s = 0
                        h += 75
                    if h == 150:
                        h = 0
            else:
                if self.turn == 1:
                    self.attack(self.atk_choice)
                self.HUD.fill(GREY)

            pygame.display.flip()
