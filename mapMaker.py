import pygame


pygame.init()

size = width, height = 600, 700

pygame.display.set_mode(size)

gameRun = True

while gameRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False


pygame.quit()