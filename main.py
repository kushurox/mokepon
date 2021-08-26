import pygame
from pygame.time import Clock
import utils.color as colors  # Use the colors.py to define ur color
from spriteClasses.characters import Player  # All the Game entities will be defined here
from utils.constants import window_size
from utils.terrains import GameTerrain, Terrains, load_map
from utils.constants import default_sprite_res

pygame.init()

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("mokepon")  # Setting up screen title

run = True
clock = Clock()
gameMenu = True

whole_map = load_map('maps/testmap.csv')

characters = pygame.sprite.Group()  # Will contain all game entities and updates them
start_tile = whole_map.get_terrain(window_size[0] // 2, window_size[1] // 2)

p1 = Player(colors.WHITE, start_tile)  # Making a Player entity
characters.add(p1)  # Adding it to the all_sprites container

menuCanvas = pygame.Surface(window_size)
move_player = False
#
# while gameMenu:
#     for event in pygame.event.get():

screen.fill(colors.BLACK)

move_key = None

ms = 0.5


def move(t, mk=None):
    global ms
    ms -= t

    if move_player and ms <= 0:
        coords = p1.get_move(mk)
        t = whole_map.get_terrain(*coords)
        if t:
            p1.move(t)
        ms = 0.5


while run:
    dt = clock.tick(30) / 1000
    for event in pygame.event.get():  # Looping through all events
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN and event.key in p1.movementX:
            move_player = True
            move_key = event.key
        elif event.type == pygame.KEYUP and event.key in p1.movementX:
            move_player = False

    characters.update(dt)  # Updates all the entities
    whole_map.draw(screen)

    characters.draw(screen)
    move(dt, move_key)

    pygame.display.flip()  # Updates the screen

pygame.quit()  # Stops Pygame
