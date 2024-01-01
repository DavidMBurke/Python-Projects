import numpy as np, pygame, settings, surface

dtype = np.dtype([
    ('index', int, (2,)),
    ('pos', int, (2,)),
    ('pheromones', int, (3,)), # also sets color. r, g, b = Return, g = food, b unassigned
    ('p1_gradient', float),
    ('p1_strength', int),
    ('p2_gradient', float),
    ('p2_strength', int),
    ('food', float),
    ('wall', bool)
])

def draw_gridlines():
    for i in range (0, settings.window[0], settings.c_size):
        pygame.draw.line(surface.grid, (100,100,100), (i, 0), (i, settings.c_rows * settings.c_size))
    for j in range (0, settings.window[1], settings.c_size):
        pygame.draw.line(surface.grid, (100,100,100), (0, j), (settings.c_cols * settings.c_size, j))

def initialize(grid_cells):
    for i in range(settings.c_cols):
        for j in range (settings.c_rows):
            index = [i,j]
            pos = [i * settings.c_size, j * settings.c_size]
            pheromones = [0, 0, 0]
            p1_gradient = 0
            p1_strength = 0
            p2_gradient = 0
            p2_strength = 0
            food = 0
            is_wall = False
            grid_cells[i, j] = (index, pos, pheromones, p1_gradient, p1_strength, p2_gradient, p2_strength, food, is_wall)
