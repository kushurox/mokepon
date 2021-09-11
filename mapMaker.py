import pickle
import pygame
from spriteClasses.container import Air
from utils.camera import EditorCamera
from utils.color import BLACK, GREEN, RED
from utils.constants import letters
import os
import numpy as np

from utils.terrains import Terrain


class Containers(pygame.sprite.Group):
    current_tile = None

    def get_current_tile(self):
        return self.current_tile


class Assets(Containers):
    pass


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

SELECTED_TILE = None

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
assets = Assets()

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
    pygame.K_RIGHT: cam.right,
}

CONTEXT = 0

to_save = False

f_name = pygame.font.Font('assets/fonts/firasans-book.ttf', 32)
filename_s = ""

save_canvas = pygame.Surface((400, 200))
save_canvas.fill(GREEN)


def save(fn):
    global to_save
    map_ = []
    to_save = True
    cnt = 0
    sprites = containers.sprites()
    for i in sprites:
        map_.append(i.block_id)
    with open(fn, "wb") as fp:
        pickle.dump(np.array(map_).reshape((canvas_height // 50, canvas_width // 50)), fp)


while gameRun:
    mx, my = pygame.mouse.get_pos()
    if to_save:
        CONTEXT = 2
    elif mx > 600:
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

        if CONTEXT == 1:  # Checks if he is selecting any asset
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    assets.update(mx, my)
                    SELECTED_TILE = assets.get_current_tile()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                to_save = True

        elif CONTEXT == 2:
            if event.type == pygame.KEYUP:
                if event.unicode not in letters:
                    if event.key == pygame.K_BACKSPACE:
                        save_canvas.fill(GREEN)
                        filename_s = filename_s[:-1]
                    elif event.key == pygame.K_RETURN:
                        save(filename_s + ".pickle")
                        to_save = False

                else:
                    filename_s += event.unicode

                filename = f_name.render(filename_s, True, BLACK, GREEN)
                save_canvas.blit(filename, (50, 70))

            f = pygame.font.Font("assets/fonts/firasans-book.ttf", 32)
            text = f.render("File Name", True, BLACK, GREEN)
            textRect = text.get_rect()

            save_canvas.blit(text, (150, 0))

        else:
            if SELECTED_TILE and event.type == pygame.MOUSEBUTTONDOWN:  # Checks if a mouse button was pressed
                if event.button == 3:
                    rmb_d = True
                    a = containers.get_current_tile()
                    a.reset_stats()
                else:
                    lmb_d = True
                    a = containers.get_current_tile()
                    a.occupied = True
                    a.set_terrain(SELECTED_TILE)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    rmb_d = False
                else:
                    lmb_d = False
            elif event.type == pygame.MOUSEMOTION:
                containers.update((mx + cam.x_offset, my + cam.y_offset))
                containers.draw(canvas)
                if rmb_d:  # Right click check
                    a = containers.get_current_tile()
                    a.reset_stats()
                elif lmb_d:  # Left Click
                    a = containers.get_current_tile()
                    a.occupied = True
                    a.set_terrain(SELECTED_TILE)

    screen.fill(BLACK)
    screen.blit(canvas, (0, 0), (cam.begin_x, cam.begin_y, width - 100, height))
    assets.draw(screen)

    if CONTEXT == 2:
        screen.blit(save_canvas, (100, 200))

    pygame.display.flip()

pygame.quit()
