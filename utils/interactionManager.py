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
    def __init__(self, screen, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.screen = screen

        self.start_battle()

    def start_battle(self):
        print(f"Battle occurred between {self.p1} and {self.p2}")