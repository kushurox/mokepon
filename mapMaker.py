import pygame
from spriteClasses.container import Air
from utils.color import BLACK


class Containers(pygame.sprite.Group):
    current_tile = None

    def get_current_tile(self):
        return self.current_tile


pygame.init()

size = width, height = 600, 600

screen = pygame.display.set_mode(size)

gameRun = True

containers = Containers()

y = 0

for i in range(height//50):
    x = 0
    for j in range(width//50):
        containers.add(Air((50, 50), (0, 0, 55), (x, y)))
        x += 50
    y += 50


while gameRun:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                print("Ran")
                a = containers.get_current_tile()
                print(a.occupied)
                a.occupied = False
            elif event.button == 1:
                a = containers.get_current_tile()
                print(containers.sprites().index(a))
                a.occupied = True
                a.image.fill(BLACK)

    containers.update(pygame.mouse.get_pos())
    screen.fill(BLACK)
    containers.draw(screen)
    pygame.display.flip()


pygame.quit()