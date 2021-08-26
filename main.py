import pygame
from pygame.time import Clock

import utils.color as colors                 # Use the colors.py to define ur color
from spriteClasses.characters import Player  # All the Game entities will be defined here
from utils.constants import window_size
from utils.terrains import load_map

pygame.init()
pygame.mixer.init()

bgm = pygame.mixer.Sound("assets/misc/bgm.wav")
bgm.play(-1)

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("mokepon")        # Setting up screen title

run = True
clock = Clock()
gameMenu = True

whole_map = load_map('maps/testmap.csv')

characters = pygame.sprite.Group()            # Will contain all game entities and updates them

p1 = Player(colors.WHITE, whole_map)         # Making a Player entity
characters.add(p1)                            # Adding it to the all_sprites container

menuCanvas = pygame.Surface(window_size)

ts = 500
ws = 50
pmx = False
pmy = False
pkx = None
pky = None
wt = (1 / ws) * 5

screen.fill(colors.BLACK)

movementX = {
    pygame.K_a: -ws,
    pygame.K_d: ws
}

movementY = {
    pygame.K_w: -ws,
    pygame.K_s: ws
}

while run:
    dt = clock.tick(30)
    for event in pygame.event.get():            # Looping through all events
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN and event.key in movementX:
            pmx = True
            pkx = event.key
        elif event.type == pygame.KEYDOWN and event.key in movementY:
            pmy = True
            pky = event.key
        elif event.type == pygame.KEYUP and event.key in movementX:
            pmx = False
        elif event.type == pygame.KEYUP and event.key in movementY:
            pmy = False

    characters.update(dt)                        # Updates all the entities
    whole_map.draw(screen)
    p1.move(pmx, pmy, pkx, pky, movementX, movementY, wt)

    characters.draw(screen)

    pygame.display.flip()                        # Updates the screen

pygame.quit()                                    # Stops Pygame
