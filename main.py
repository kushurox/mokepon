import pygame
from spriteClasses.characters import Player     # All the Game entities will be defined here
import utils.color as colors                    # Use the colors.py to define ur color

pygame.init()

size = height, width = 800, 600                 # Setting the screen resolution

all_sprites = pygame.sprite.Group()             # Will contain all game entities and updates them

p1 = Player(colors.WHITE, (100, 100))           # Making a Player entity
all_sprites.add(p1)                             # Adding it to the all_sprites container

screen = pygame.display.set_mode(size)
pygame.display.set_caption("mokepon")           # Setting up screen title

run = True

while run:
    for event in pygame.event.get():            # Looping through all events
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()                        # Updates all the entities
    all_sprites.draw(screen)                    # Draws all the entities on the screen
    pygame.display.flip()                       # Updates the screen

pygame.quit()                                   # Stops Pygame
