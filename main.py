import pygame
from pygame.time import Clock

import utils.color as colors  # Use the colors.py to define ur color
from spriteClasses.characters import Player, NPC  # All the Game entities will be defined here
from utils.camera import GameCamera
from utils.constants import window_size
from utils.interactionManager import InteractionManager
from utils.terrains import load_map

pygame.init()
# pygame.mixer.init()
#
# bgm = pygame.mixer.Sound("assets/misc/bgm.wav")
# bgm.play(-1)


screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("mokepon")  # Setting up screen title

run = True
clock = Clock()
gameMenu = True

im = InteractionManager(screen)

whole_map = load_map('maps/fullmap.pickle')

characters = pygame.sprite.Group()  # Will contain all game entities and updates them

camera = GameCamera(0, 0)

npcs = pygame.sprite.Group()

p1 = Player(colors.WHITE, whole_map, 1, camera)  # Making a Player entity
terrain = whole_map.get_terrain(100, 100)
npc1 = NPC(terrain, whole_map, ["hello", "hi", "kushurox"])
npcs.add(npc1)
menuCanvas = pygame.Surface((1400, 900))

ts = 500
ws = 50
pmx = False
pmy = False
pkx = None
pky = None
wt = (1 / ws) * 7

screen.fill(colors.BLACK)

movementX = {
    pygame.K_a: -ws,
    pygame.K_d: ws
}

movementY = {
    pygame.K_w: -ws,
    pygame.K_s: ws
}


def mainmenu():
    global run
    main_menu = True

    menu_map = load_map("maps/fullmap.pickle")

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

while run:
    dt = clock.tick(30)
    for event in pygame.event.get():  # Looping through all events
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key in movementX:
            p1.bobs[True] = p1.character_sprite1[event.key]
            p1.bobs[False] = p1.character_sprite2[event.key]
            p1.next_bob = 0
            pmx = True
            pkx = event.key
        elif event.type == pygame.KEYDOWN and event.key in movementY:
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

    p1.update(dt)
    whole_map.draw(menuCanvas)

    screen.fill(colors.BLACK)

    p1.move(pmx, pmy, pkx, pky, movementX, movementY, wt)
    p1.draw(menuCanvas)
    npcs.draw(menuCanvas)
    screen.blit(menuCanvas, (0, 0), (camera.begin_x, camera.begin_y, camera.end_x, camera.end_y))
    im.update()

    pygame.display.flip()  # Updates the screen

pygame.quit()  # Stops Pygame
