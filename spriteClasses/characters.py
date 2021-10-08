import pickle
from itertools import cycle
from os.path import exists
from typing import Callable

import pygame

from utils.camera import GameCamera
from utils.color import BLACK
from utils.constants import window_size, kd2, kd4
from utils.terrains import GameTerrain, Terrains

dialogue_font = pygame.font.Font("assets/fonts/VPPixel-Simplified.otf", 32)


class Player(pygame.sprite.Sprite):

    flags = {}

    identity = "Protagonist-san"
    mokepon = None

    next_bob = 300

    gender = None

    movementX = {
        pygame.K_a: -48,
        pygame.K_d: 52,
        pygame.K_w: 0,
        pygame.K_s: 0
    }

    area = None
    moving = False
    tt = None
    status = False
    PLAYER_SIZE = (50, 50)
    bobs = {}
    facing_tile = None

    def __init__(self, color: tuple, whole_area: Terrains, gender: int, camera: GameCamera):
        super(Player, self).__init__()

        if exists("gamestate"):
            with open("gamestate", "rb") as fp:
                self.flags = pickle.load(fp)
        else:
            with open("gamestate", "wb") as fp:
                self.flags = {"defeat_mihir": 0, "defeat_kushal": 0, "talk_kushal": 0}
                pickle.dump(self.flags, fp)

        self.camera = camera

        self.gender = gender
        if gender == 1:  # male
            self.bobs[True] = pygame.image.load("assets/char_animation/boy_idle/mpknboy1.png")
            self.bobs[False] = pygame.image.load("assets/char_animation/boy_idle/mpknboy2.png")
            self.character_sprite1 = {
                pygame.K_a: pygame.image.load("assets/char_animation/boy_move/boyl1.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/boy_move/boyr1.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/boy_move/boyb1.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/boy_move/boyf1.png"),
                -1: pygame.image.load("assets/char_animation/boy_idle/mpknboy1.png")
            }
            self.character_sprite2 = {
                pygame.K_a: pygame.image.load("assets/char_animation/boy_move/boyl2.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/boy_move/boyr2.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/boy_move/boyb2.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/boy_move/boyf2.png"),
                -1: pygame.image.load("assets/char_animation/boy_idle/mpknboy2.png")
            }
        elif gender == 0:
            self.bobs[True] = pygame.image.load("assets/char_animation/girl_idle/mpkngirl1.png")
            self.bobs[False] = pygame.image.load("assets/char_animation/girl_idle/mpkngirl2.png")
            self.character_sprite1 = {
                pygame.K_a: pygame.image.load("assets/char_animation/girl_move/girll1.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/girl_move/girlr1.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/girl_move/girlb1.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/girl_move/girlf1.png"),
                -1: pygame.image.load("assets/char_animation/girl_idle/mpkngirl1.png")
            }
            self.character_sprite2 = {
                pygame.K_a: pygame.image.load("assets/char_animation/girl_move/girll2.png"),
                pygame.K_d: pygame.image.load("assets/char_animation/girl_move/girlr2.png"),
                pygame.K_w: pygame.image.load("assets/char_animation/girl_move/girlb2.png"),
                pygame.K_s: pygame.image.load("assets/char_animation/girl_move/girlf2.png"),
                -1: pygame.image.load("assets/char_animation/girl_idle/mpkngirl2.png")
            }

        self.image = self.bobs[False]
        self.image = pygame.transform.scale(self.image, self.PLAYER_SIZE)

        self.area = whole_area

        self.current_tile = whole_area.get_terrain(window_size[0] // 2, window_size[1] // 2)

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.current_tile.rect.x, self.current_tile.rect.y

    def update(self, *args, **kwargs) -> None:
        dt = args[0]
        self.next_bob -= dt
        if self.next_bob <= 0:
            self.image = self.bobs[self.status]
            self.status = not self.status
            self.next_bob = 300

    def move(self, pmx, pmy, pkx, pky, movementX, movementY, wt):

        if pmx and not pmy:
            x = movementX[pkx]
            x *= wt
            dx = self.rect.x + x
            if x < 0:
                contact_tile = self.area.get_terrain(dx, self.rect.y + 25)
            else:
                contact_tile = self.area.get_terrain(dx + 50, self.rect.y + 25)

            self.facing_tile = contact_tile

            if self.target(contact_tile):
                self.rect.x = dx
                self.camera.begin_x = self.rect.x - 300

        if pmy and not pmx:
            y = movementY[pky]
            y *= wt
            dy = self.rect.y + y
            if y < 0:
                contact_tile = self.area.get_terrain(self.rect.x + 25, dy)
            else:
                contact_tile = self.area.get_terrain(self.rect.x + 25, dy + 50)

            self.facing_tile = contact_tile

            if self.target(contact_tile):
                self.rect.y = dy
                self.camera.begin_y = self.rect.y - 300

        self.current_tile = self.area.get_terrain(self.rect.x + 25 + self.camera.x_offset,
                                                  self.rect.y + 25 + self.camera.y_offset)

    @staticmethod
    def target(terrain: GameTerrain):
        if terrain:
            return not terrain.collide

    def get_move(self, key):
        if key in self.movementX:
            return self.current_tile
        return False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class NPC(pygame.sprite.Sprite):
    chatbox = pygame.image.load("assets/misc/g2429.png")
    text = dialogue_font.render("Default", False, BLACK)
    start_action = None
    start_action_args = []
    end_action = None
    end_action_args = None
    mokepon = None
    victory_action = None
    victory_action_args = None
    defeat_action = None
    defeat_args = None

    def __init__(self, terrain: GameTerrain, area: Terrains, dialogues: list, identity: int, image_name, name):
        super(NPC, self).__init__()
        self.area = area
        dialogues.append(False)  # End of Interaction
        self.area.terrain_to_entity[terrain] = self
        self.dialogues = cycle(dialogues)
        self.identity = name
        if exists(f"assets/dialogue_Assets/{name}.png"):
            self.dialogue_image = pygame.image.load(f"assets/dialogue_Assets/{name}.png")
        else:
            print(f"assets/dialogue_Assets/{name}.png not found")
        self.current_tile = terrain
        self.current_tile.collide = True
        self.image = pygame.image.load(f"assets/npcs/{image_name}.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = terrain.rect.x, terrain.rect.y
        self.id = identity

    def interaction(self, context, event, screen, *args):
        screen.blit(self.chatbox, (0, 490))
        screen.blit(self.text, (32, 522))
        res = False

        if event and event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            if self.start_action:
                res = self.start_action(self, *self.start_action_args)
            d = next(self.dialogues)
            context.event = None
            if d:
                self.text = dialogue_font.render(d, False, BLACK)
            else:
                if self.end_action:
                    res = self.end_action(self, *self.end_action_args)
                context.set_interaction(None)
            return res

    def set_start_action(self, action: Callable = None, *args):
        self.start_action = action
        self.start_action_args = args

    def set_end_action(self, action: Callable = None, *args):
        self.end_action = action
        self.end_action_args = args

    def set_victory_action(self, action: Callable, *args):
        self.victory_action = action
        self.victory_action_args = args

    def set_defeat_action(self, action: Callable, *args):
        self.defeat_action = action
        self.defeat_args = args


def kushuroxEvil(npc: NPC, *args):
    if not args[0].flags["defeat_kushal"]:
        npc.dialogues = cycle(kd2 + [False])
    return {'event': "battle", "player1": args[0], "player2": npc}


def kushuroxChild(npc: NPC, *args):
    if not args[0].flags["defeat_mihir"]:
        args[0].flags["talk_kushal"] = 1
        with open("gamestate", "wb") as fp:
            pickle.dump(args[0].flags, fp)

    else:
        npc.set_end_action(kushuroxEvil, *args)
        npc.end_action(npc, *args)
        npc.set_start_action(None)


def kushuroxLose(npc: NPC, *args):
    npc.dialogues = cycle(kd4 + [False])
    args[0].flags["defeat_kushal"] = 1
    with open("gamestate", "wb") as fp:
        pickle.dump(args[0].flags, fp)
    return ["What!?", "I have lost!?", "The Great kushurox!?",
            "You will pay for this!", "...", "...", "kushurox has disappeared"]


def kushuroxWin(npc: NPC):
    return ["You were 100 years early to take me on", "Better luck next time kid",
            "After all it is i kushurox", "You never Stood a chance", "Farewell"]


def meerBattle(npc: NPC, *args):
    if args[0].flags["talk_kushal"]:
        return {'event': "battle", "player1": args[0], "player2": npc}


def meerWin(npc: NPC):
    return [".......", "--------", "........"]


def meerLose(npc, *args):
    args[0].flags["defeat_mihir"] = 1
    with open("gamestate", "wb") as fp:
        pickle.dump(args[0].flags, fp)
    return ["Final", "Warning", "Stop"]