import math, random, numpy as np, pygame
import settings, colors

# ant datatype
dtype = np.dtype([
    ('pos', float, (2,)),
    ('index', int, (2,)),
    ('direction', float),
    ('food', float),
    ('color', int)
])


def update_pos(ants, grid_cells, delta_time):

    # Create array of random values from -1 to 1
    rand_array = (np.random.rand(ants['direction'].shape[0]) * 2 - 1)
    # Identify ants sitting on food
    ants_on_food = np.array([grid_cells[x,y]['food'] > 0 for x,y in ants['index']])
    # Increase ant food and decrease cell food
    # TODO currently flubbing this, need actually subtract food from grid and add to ants
    ants['food'][ants_on_food] += 5
    ants['color'][ants_on_food] = colors.green
    # Identify ants with food
    has_food = ants['food'] > 100
    # Aim ants toward pheromone 1 ('exploring' pheromone) plus a random value if they have food
    p1_strength = np.array([grid_cells[x,y]['p1_strength'] for x,y in ants['index']])
    seeks_home = (has_food) & (p1_strength > 0)
    ants['direction'][seeks_home] = np.array([grid_cells[x,y]['p1_gradient'] for x,y in ants['index'][seeks_home]])
    ants['direction'][seeks_home] += rand_array[seeks_home] * delta_time * 20
    # Aim ants toward pheromone 2 (food) if they do not have food
    p2_strength = np.array([grid_cells[x,y]['p2_strength'] for x,y in ants['index']])
    seeks_food = (~has_food) & (p2_strength > 0)
    ants['direction'][seeks_food] = np.array([grid_cells[x,y]['p2_gradient'] for x,y in ants['index'][seeks_food]])
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
    for index, ant in np.ndenumerate(ants):
        x, y = int(ant['pos'][0]), int(ant['pos'][1])
        pixels[x,y] = ant['color']
        pixels[x+1,y] = ant['color']
        pixels[x,y+1] = ant['color']
        pixels[x+1,y+1] = ant['color']
        pixel_alphas[x,y] = colors.blue
    # Delete canvas variables to release lock on canvas
    del pixels
    del pixel_alphas

# Increase pheromone at index position
def drop_pheromones(ants, grid_cells):
    # Ants looking for food
    exploring_ants = ants[ants['food'] < 50]
    for i, j in exploring_ants['index']:
        grid_cells[i, j]['pheromones'][0] += settings.p1_increase

    # Ants that have food to return
    ants_with_food = ants[ants['food'] > 50]
    for i, j in ants_with_food['index']:
        grid_cells[i, j]['pheromones'][1] += settings.p2_increase

#Initialize ants array
def initialize(ants):
    for i in range(settings.num_ants):
        pos = (settings.window[0] * .5, settings.window[1] * .5)
        index = (pos[0] // settings.c_size, pos[1] // settings.c_size)
        direction = (random.random() * 2 * math.pi)
        food = 0
        color = colors.gray
        ants[i] = (pos, index, direction, food, color)