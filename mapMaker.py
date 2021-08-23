import pygame
from spriteClasses.container import Air
from utils.camera import EditorCamera
from utils.color import BLACK
import os

from utils.terrains import Terrain


class Containers(pygame.sprite.Group):
    current_tile = None

    def get_current_tile(self):
        return self.current_tile




pygame.init()

size = width, height = 700, 600

screen = pygame.display.set_mode(size)

gameRun = True

containers = Containers()

canvas_size = canvas_width, canvas_height = 1400, 900
canvas = pygame.Surface(canvas_size)

cam = EditorCamera(0, 0)

lmb_d = False
rmb_d = False

y = 0

for i in range(canvas_height // 50):  # Loads Map Area
    x = 0
    for j in range(canvas_width // 50):
        containers.add(Air((50, 50), (0, 0, 55), (x, y)))
        x += 50
    y += 50


ay = 0
ax = 600

surfaces = os.listdir("assets/surfaces")
assets = pygame.sprite.Group()

total = len(surfaces)

for i in surfaces:
    t = Terrain(i)
    t.rect.x = ax
    t.rect.y = ay
    assets.add(t)
    if ax == 650:
        ax = 600
        ay += 50
    ax += 50


cam_y_offset = 0
cam_x_offset = 0


funcs = {
    pygame.K_UP: cam.up,
    pygame.K_DOWN: cam.down,
    pygame.K_LEFT: cam.left,
    pygame.K_RIGHT: cam.right
}



CONTEXT = 0

while gameRun:
    mx, my = pygame.mouse.get_pos()
    if mx > 600:
        CONTEXT = 1
    else:
        CONTEXT = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRun = False

        if event.type == pygame.KEYUP:
            task = funcs.get(event.key)
            if task:
                task()


        if CONTEXT:  # Checks if he is selecting any asset
            pass
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:  # Checks if a mouse button was pressed
                if event.button == 3:
                    rmb_d = True
                    a = containers.get_current_tile()
                    a.occupied = False
                else:
                    lmb_d = True
                    a = containers.get_current_tile()
                    a.occupied = True
                    a.image.fill(BLACK)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    rmb_d = False
                else:
                    lmb_d = False
            elif event.type == pygame.MOUSEMOTION:
                if rmb_d:  # Right click check
                    a = containers.get_current_tile()
                    a.occupied = False
                elif lmb_d:  # Left Click
                    a = containers.get_current_tile()
                    a.occupied = True
                    a.image.fill(BLACK)

    containers.update(pygame.mouse.get_pos())
    screen.fill(BLACK)
    screen.blit(canvas, (0, 0), (cam.begin_x, cam.begin_y, width-100, height))
    containers.draw(canvas)
    assets.draw(screen)
    pygame.display.flip()

pygame.quit()
