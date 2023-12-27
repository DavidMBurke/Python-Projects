import math, random, numpy as np, pygame, settings

dtype = np.dtype([
    ('pos', float, (2,)),
    ('index', int, (2,)),
    ('direction', float),
    ('food', float)
])

def update_pos(ants, grid_cells, delta_time):
    rand_array = (np.random.rand(ants['direction'].shape[0]) * 2 - 1)
    ants['direction'] += rand_array * delta_time * 10
    x = np.cos(ants['direction']) * delta_time * settings.ant_speed
    y = np.sin(ants['direction']) * delta_time * settings.ant_speed
    movement = np.column_stack((x,y))
    new_pos = ants['pos'] + movement
    new_index = np.floor(new_pos / settings.c_size).astype(int)
    can_move = np.array([grid_cells[x,y]['wall'] == False for x,y in new_index])
    ants['pos'][can_move] = new_pos[can_move]
    ants['index'][can_move] = new_index[can_move]
    ants['direction'][~can_move] += rand_array[~can_move] * math.pi

def draw(ants, surface):
    pixels = pygame.surfarray.pixels2d(surface)
    pixel_alphas = pygame.surfarray.pixels_alpha(surface)
    pixels.fill(0)
    pixel_alphas.fill(0)
    for i,j in ants['pos']:
        x, y = int(i), int(j)
        pixels[x,y] = 16777215
        pixel_alphas[x,y] = 255
    del pixels
    del pixel_alphas

def drop_pheromones(ants, grid_cells):
    for i, j in ants['index']:
        grid_cells[i, j]['pheromones'][0] += settings.p_strength

def initialize(ants):
    for i in range(settings.num_ants):
        pos = (settings.window[0] * .5, settings.window[1] * .5)
        index = (pos[0] // settings.c_size, pos[1] // settings.c_size)
        direction = (random.random() * 2 * math.pi)
        food = 0
        ants[i] = (pos, index, direction, food)