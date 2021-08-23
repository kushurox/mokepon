import pygame
from pygame.time import Clock
import utils.color as colors  # Use the colors.py to define ur color
from spriteClasses.characters import Player  # All the Game entities will be defined here

pygame.init()

size = width, height = 1400, 800  # Setting the screen resolution

all_sprites = pygame.sprite.Group()  # Will contain all game entities and updates them

p1 = Player(colors.WHITE, (250, 250))  # Making a Player entity
all_sprites.add(p1)  # Adding it to the all_sprites container

screen = pygame.display.set_mode(size)
pygame.display.set_caption("mokepon")  # Setting up screen title

run = True
clock = Clock()
while run:
    dt = clock.tick(30)/1000
    for event in pygame.event.get():  # Looping through all events
        if event.type == pygame.QUIT:
            run = False

    screen.fill(colors.BLACK)
    all_sprites.update(dt)  # Updates all the entities
    all_sprites.draw(screen)  # Draws all the entities on the screen
    pygame.display.flip()  # Updates the screen

pygame.quit()  # Stops Pygame
