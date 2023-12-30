import math, random, numpy as np, pygame, settings

# ant datatype
dtype = np.dtype([
    ('pos', float, (2,)),
    ('index', int, (2,)),
    ('direction', float),
    ('food', float)
])


def update_pos(ants, grid_cells, delta_time):

    # Create array of random values from -1 to 1
    rand_array = (np.random.rand(ants['direction'].shape[0]) * 2 - 1)
    # Identify ants with food
    has_food = ants['food'] > 50
    # Aim ants toward pheromone 1 ('exploring' pheromone) plus a random value if they have food
    ants['direction'][has_food] = np.array([grid_cells[x,y]['p1_gradient'] for x,y in ants['index'][has_food]])
    ants['direction'][has_food] += rand_array[has_food] * delta_time * 20
    # Apply random motion to all ants
    ants['direction'] += rand_array * delta_time * 20
    # Convert direction from radians to x and y displacement
    x = np.cos(ants['direction']) * delta_time * settings.ant_speed
    y = np.sin(ants['direction']) * delta_time * settings.ant_speed
    movement = np.column_stack((x,y))
    new_pos = ants['pos'] + movement
    # Determine new index. Apply movement or prevent movement and assign random new direction if new grid has wall
    # TODO stop ants being able to move diagonally if horizontal and vertical blocked
    new_index = np.floor(new_pos / settings.c_size).astype(int)
    can_move = np.array([grid_cells[x,y]['wall'] == False for x,y in new_index])
    ants['pos'][can_move] = new_pos[can_move]
    ants['index'][can_move] = new_index[can_move]
    ants['direction'][~can_move] += rand_array[~can_move] * math.pi

# Retrieve pixel values
def draw(ants, surface):
    # Access canvas
    pixels = pygame.surfarray.pixels2d(surface)
    pixel_alphas = pygame.surfarray.pixels_alpha(surface)
    # Clear canvas and make transparent
    pixels.fill(0)
    pixel_alphas.fill(0)
    # Place white dots and make opaque
    for i,j in ants['pos']:
        x, y = int(i), int(j)
        pixels[x,y] = 16777215 # red * 2^16 + g * 2^8 + b
        pixel_alphas[x,y] = 255
    # Delete canvas variables to release lock on canvas
    del pixels
    del pixel_alphas

# Increase pheromone at index position
def drop_pheromones(ants, grid_cells):
    for i, j in ants['index']:
        grid_cells[i, j]['pheromones'][0] += settings.p_strength

#Initialize ants array
def initialize(ants):
    for i in range(settings.num_ants):
        pos = (settings.window[0] * .5, settings.window[1] * .5)
        index = (pos[0] // settings.c_size, pos[1] // settings.c_size)
        direction = (random.random() * 2 * math.pi)
        food = 0
        ants[i] = (pos, index, direction, food)