from math import sin, cos, radians

import pygame
from pygame.time import Clock

import utils.color as colors  # Use the colors.py to define ur color
from spriteClasses.characters import Player, NPC, kushuroxChild, \
    kushuroxWin, kushuroxLose, meerBattle, meer  # All the Game entities will be defined here
from spriteClasses.mokepons import Destroyer, Byru, Orb
from utils.camera import GameCamera
from utils.constants import window_size, kd1, kd3
from utils.interactionManager import InteractionManager, Battle
from utils.terrains import load_map

pygame.init()

battle_font = pygame.font.Font("assets/fonts/VPPixel-Simplified.otf", 24)

song = pygame.mixer.Sound("assets/music/bgm.mp3")
song.play(-1)

song.set_volume(0.3)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("mokepon")  # Setting up screen title

run = True
clock = Clock()
gameMenu = True

im = InteractionManager(screen)

whole_map = load_map('maps/fullmapt.pickle')

characters = pygame.sprite.Group()  # Will contain all game entities and updates them

camera = GameCamera(0, 0)

# PLAYER INIT
p1 = Player(colors.WHITE, whole_map, 1, camera)  # Making a Player entity
p1.mokepon = Byru()

# PLAYER INIT END

# npc pos
pos1 = whole_map.get_terrain(150, 800)
pos2 = whole_map.get_terrain(1150, 750)
# npc pos end


menuCanvas = pygame.Surface((1400, 900))

#  NPC INIT
npcs = pygame.sprite.Group()
# -----------------------#
kushurox = NPC(pos1, whole_map, kd1, 2, "kosupai", "kushurox")
npcs.add(kushurox)
kushurox.set_start_action(kushuroxChild, p1)
kushurox.set_victory_action(kushuroxWin)
kushurox.set_defeat_action(kushuroxLose, p1)
kushurox.mokepon = Destroyer()
# -----------------------#
meep = NPC(pos2, whole_map, kd3, 1, "mierpng", "mihir")
meep.set_end_action(meerBattle, p1)
meep.set_victory_action(meer)
meep.set_defeat_action(meer, p1)
meep.mokepon = Orb()
npcs.add(meep)
# NPC INIT END


# MOVEMENT INIT
ts = 500
ws = 50
pmx = False
pmy = False
pkx = None
pky = None
wt = (1 / ws) * 7
movementX = {
    pygame.K_a: -ws,
    pygame.K_d: ws
}

movementY = {
    pygame.K_w: -ws,
    pygame.K_s: ws
}
# MOVEMENT INIT END

screen.fill(colors.BLACK)

battle = False
res = False


def loading_screen():
    angular_vel = 90  # per second
    angle = 0
    screen.fill(colors.DEFAULT_CONTAINER)
    dt = clock.tick(60) / 1000
    displaybox = pygame.Surface([60, 60])
    while angle >= -360:
        displaybox.fill(colors.DEFAULT_CONTAINER)
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            pass

        a = radians(angle)
        x, y = 325 + (cos(a) * 100), 325 + (sin(a) * 100)
        pygame.draw.circle(screen, colors.GREEN, (x, y), 5)
        p = str(-(angle * 100) // 360) + "%"
        displaybox.blit(battle_font.render(p, False, colors.WHITE), (0, 0))
        screen.blit(displaybox, (300, 300))
        angle -= angular_vel * dt
        pygame.display.flip()


def mainmenu():
    global run
    main_menu = True

    menu_map = load_map("maps/fullmapt.pickle")

    map_canvas = pygame.Surface((650, 300))
    map_canvas.fill(colors.BLUE)

    start_x = 0

    option_font = pygame.font.Font("assets/fonts/VPPixel-Simplified.otf", 50)
    start_game = option_font.render("Start Game", False, colors.HOVER_CONTAINER)
    start_game_rect = start_game.get_rect()
    start_game_rect.x = 100
    start_game_rect.y = 100

    while main_menu:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main_menu = False
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                if start_game_rect.collidepoint(mx, my):
                    start_game = option_font.render("Start Game", False, colors.RED)
                else:
                    start_game = option_font.render("Start Game", False, colors.HOVER_CONTAINER)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    main_menu = False

        screen.fill(colors.DEFAULT_CONTAINER)
        screen.blit(map_canvas, (0, 350), (start_x, 0, 650, 300))
        screen.blit(start_game, (start_game_rect.x, start_game_rect.y))
        start_x += 2
        if start_x >= 650:
            start_x = -650
        menu_map.draw(map_canvas)
        pygame.display.flip()


mainmenu()
loading_screen()

while run:
    dt = clock.tick(30)
    for event in pygame.event.get():  # Looping through all events
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key in movementX and not im.interaction:
            p1.bobs[True] = p1.character_sprite1[event.key]
            p1.bobs[False] = p1.character_sprite2[event.key]
            p1.next_bob = 0
            pmx = True
            pkx = event.key
        elif event.type == pygame.KEYDOWN and event.key in movementY and not im.interaction:
            p1.bobs[True] = p1.character_sprite1[event.key]
            p1.bobs[False] = p1.character_sprite2[event.key]
            p1.next_bob = 0
            pmy = True
            pky = event.key
        elif event.type == pygame.KEYUP and event.key in movementX:
            pmx = False
        elif event.type == pygame.KEYUP and event.key in movementY:
            pmy = False

        elif event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            facing_tile = p1.facing_tile
            entity = whole_map.terrain_to_entity.get(facing_tile)
            if entity:
                im.set_interaction(entity.interaction)
                im.event = event

    if not pmx and not pmy:
        p1.bobs[True] = p1.character_sprite1[-1]
        p1.bobs[False] = p1.character_sprite2[-1]

    if not battle:
        p1.update(dt)
        whole_map.draw(menuCanvas)

        screen.fill(colors.BLACK)

        p1.move(pmx, pmy, pkx, pky, movementX, movementY, wt)
        p1.draw(menuCanvas)
        npcs.draw(menuCanvas)
        screen.blit(menuCanvas, (0, 0), (camera.begin_x, camera.begin_y, camera.end_x, camera.end_y))
        res = im.update()
    if res:
        if res['event'] == "battle":
            battle = True

            print(f"Player 2 id {res['player2'].id}")
            if res['player2'].id == 2:
                print("Music played")
                song.stop()
                song = pygame.mixer.Sound("assets/music/kushurox.mp3")
                song.play(-1)
                song.set_volume(0.3)

            b = Battle(screen, res["player1"], res["player2"])
            song.stop()
            song = pygame.mixer.Sound("assets/music/bgm.mp3")
            song.play(-1)

            song.set_volume(0.3)

            res = False
            battle = False

    pygame.display.flip()  # Updates the screen

pygame.quit()  # Stops Pygame
