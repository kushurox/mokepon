import pygame

from utils.color import RED

clock = pygame.time.Clock()


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


class Battle:
    battle = True
    bg = pygame.image.load("assets/battle_assets/battle.png")

    def __init__(self, screen, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.mokepon1 = p1.mokepon
        self.mokepon2 = p2.mokepon
        self.screen = screen

        self.start_battle()

    def start_battle(self):
        while self.battle:
            dt = clock.tick(30)
            for event in pygame.event.get():
                print(event)

            self.screen.blit(self.bg, (0, 0))
            self.screen.blit(self.mokepon1.image, (50, 250))
            self.screen.blit(self.mokepon2.image, (400, 50))
            pygame.display.flip()
