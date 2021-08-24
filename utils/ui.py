import pygame

s = pygame.Surface([10, 10])
sa = pygame.surfarray.array2d(s)
print(sa.shape)