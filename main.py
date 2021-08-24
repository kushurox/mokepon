import pygame
from pygame.time import Clock
import utils.color as colors  # Use the colors.py to define ur color
from spriteClasses.characters import Player  # All the Game entities will be defined here
from utils.constants import window_size, window_height, window_width

pygame.init()

characters = pygame.sprite.Group()  # Will contain all game entities and updates them

p1 = Player(colors.WHITE, ((window_width // 2)-50, (window_height // 2)-50))  # Making a Player entity
characters.add(p1)  # Adding it to the all_sprites container

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("mokepon")  # Setting up screen title

run = True
clock = Clock()
gameMenu = True

menuCanvas = pygame.Surface(window_size)
#
# while gameMenu:
#     for event in pygame.event.get():
#         pass




while run:
    dt = clock.tick(30) / 1000
    for event in pygame.event.get():  # Looping through all events
        if event.type == pygame.QUIT:
            run = False

    screen.fill(colors.BLACK)
    characters.update(dt)  # Updates all the entities
    characters.draw(screen)  # Draws all the entities on the screen
    pygame.display.flip()  # Updates the screen

pygame.quit()  # Stops Pygame
