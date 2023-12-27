import pygame, math, numpy as np, time, random, scipy as sp


WINDOW = (600, 600)

#Display surfaces
screen = pygame.display.set_mode(WINDOW)
grid_surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
wall_surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
pheromone_surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
gradient_surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
ant_surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
food_surface = pygame.Surface((WINDOW), pygame.SRCALPHA)

#Constants
ANT_SIGHT = 10 #how many squares away food/pheromones detected
CELL_SIZE = 2
CELL_ROWS = WINDOW[1] // CELL_SIZE
CELL_COLS = WINDOW[0] // CELL_SIZE
NUM_ANTS = 5000
PHEROMONE_TIME = 0.5
ANT_SPEED = 20 #Ensure ant speed * max elapsed time <= cell size to prevent ants skipping squares on checks
MAX_ELAPSED_TIME = 0.05
GRADIENT_UPDATE_SPEED = 1
PHEROMONE_UPDATE_SPEED = .1 #time in seconds to decrease pheromones on a square
PHEROMONE_DECREASE_AMOUNT = 1 #amount of decrease per update
PHEROMONE_STRENGTH = 50

#setting
slotted_box = True

gradient_timer = GRADIENT_UPDATE_SPEED
pheromone_timer = PHEROMONE_UPDATE_SPEED # time until pheromone disappates by 1
prev_time = time.time()
delta_time = time.time()
pygame.init()

#Debug Settings
debug_show_pheromones = True
debug_show_grid = False # g key
debug_timed_run = False # For profiling
debug_timed_run_timer = 30.0 # For profiling
debug_show_gradient = False # v key

grid_cell_dtype = np.dtype([
    ('index', int, (2,)),
    ('pos', int, (2,)),
    ('pheromones', int, (3,)), # also sets color. r, g, b = Return, Go (follow to food), Battle
    ('food', float),
    ('wall', bool)
])

#Initialize grid
grid_cells = np.zeros((CELL_COLS, CELL_ROWS), dtype = grid_cell_dtype)
for i in range(CELL_COLS):
    for j in range (CELL_ROWS):
        index = [i,j]
        pos = [i * CELL_SIZE, j * CELL_SIZE]
        pheromones = [0, 0, 0]
        food = 0
        wall = False
        grid_cells[i, j] = (index, pos, pheromones, food, wall)

#Draw gridlines
for i in range (0, WINDOW[0], CELL_SIZE):
    pygame.draw.line(grid_surface, (100,100,100), (i, 0), (i, CELL_ROWS * CELL_SIZE))
for j in range (0, WINDOW[1], CELL_SIZE):
    pygame.draw.line(grid_surface, (100,100,100), (0, j), (CELL_COLS * CELL_SIZE, j))

#Set walls
grid_cells[:, 0:2]['wall'] = True
grid_cells[:, CELL_ROWS-2:CELL_ROWS]['wall'] = True
grid_cells[0:2, :]['wall'] = True
grid_cells[CELL_COLS - 2:CELL_COLS, :]['wall'] = True
if (slotted_box):
    half = (CELL_ROWS * .5, CELL_COLS * .5)
    grid_cells[int(half[0] - 50) : int(half[0] - 5), int(half[1] - 50)]['wall'] = True
    grid_cells[int(half[0] + 5) : int(half[0] + 50), int(half[1] - 50)]['wall'] = True
    grid_cells[int(half[0] - 50) : int(half[0] - 5), int(half[1] + 50)]['wall'] = True
    grid_cells[int(half[0] + 5) : int(half[0] + 50), int(half[1] + 50)]['wall'] = True
    grid_cells[int(half[0] - 50), int(half[1] - 50) : int(half[1] - 5)]['wall'] = True
    grid_cells[int(half[0] + 50), int(half[1] - 50) : int(half[1] - 5)]['wall'] = True
    grid_cells[int(half[0] - 50), int(half[1] + 5) : int(half[1] + 50)]['wall'] = True
    grid_cells[int(half[0] + 50), int(half[1] + 5) : int(half[1] + 50)]['wall'] = True

#Draw walls
for (x,y), cell in np.ndenumerate(grid_cells):
    if cell['wall']:
        pygame.draw.rect(wall_surface, (100, 100, 100), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

#Set food
grid_cells[10: CELL_ROWS-10,7:12]['food'] = 10

ant_dtype = np.dtype([
    ('pos', float, (2,)),
    ('index', int, (2,)),
    ('direction', float),
    ('food', float)
])

#Initialize ants
ants = np.zeros(NUM_ANTS, dtype = ant_dtype)
for i in range(NUM_ANTS):
    pos = (WINDOW[0] * .5, WINDOW[1] * .5)
    index = (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE)
    direction = (random.random() * 2 * math.pi)
    food = 0
    ants[i] = (pos, index, direction, food)

def update_ant_pos(delta_time):
    rand_array = (np.random.rand(ants['direction'].shape[0]) * 2 - 1)
    ants['direction'] += rand_array * delta_time * 10
    x = np.cos(ants['direction']) * delta_time * ANT_SPEED
    y = np.sin(ants['direction']) * delta_time * ANT_SPEED
    movement = np.column_stack((x,y))
    new_pos = ants['pos'] + movement
    new_index = np.floor(new_pos / CELL_SIZE).astype(int)
    can_move = np.array([grid_cells[x,y]['wall'] == False for x,y in new_index])
    ants['pos'][can_move] = new_pos[can_move]
    ants['index'][can_move] = new_index[can_move]
    ants['direction'][~can_move] += rand_array[~can_move] * math.pi

def ants_drop_pheromones():
    for i, j in ants['index']:
        grid_cells[i, j]['pheromones'][0] += PHEROMONE_STRENGTH
    
def update_pheromones():
    grid_cells['pheromones'] = np.clip(grid_cells['pheromones'] - PHEROMONE_DECREASE_AMOUNT, 0, 255)
    pixels = pygame.surfarray.pixels2d(pheromone_surface)
    pixel_alphas = pygame.surfarray.pixels_alpha(pheromone_surface)
    p = grid_cells['pheromones']
    f = grid_cells['food']
    colors = (p[:,:,0] << 16) + (p[:,:,1] << 8) + (p[:,:,2])
    colors[f > 0] = 16711935
    colors = np.repeat(colors, CELL_SIZE, axis = 0) #Expand to size of window
    colors = np.repeat(colors, CELL_SIZE, axis = 1)
    pixels[:] = colors
    pixel_alphas[colors != 0] = 100
    del pixels
    del pixel_alphas

kernel_side = 2 * ANT_SIGHT + 1
kernel_x = np.zeros((kernel_side, kernel_side))
kernel_x[:ANT_SIGHT, :] = 1
kernel_x[1+ANT_SIGHT:, :] = -1
kernel_y = np.zeros((kernel_side, kernel_side))
kernel_y[:,:ANT_SIGHT] = 1
kernel_y[:,1+ANT_SIGHT:] = -1

def update_gradient():
    f = grid_cells['pheromones'][:,:,0]
    
    gradient_x = sp.ndimage.convolve(f, kernel_x, mode='constant', cval = 0)
    gradient_y = sp.ndimage.convolve(f, kernel_y, mode='constant', cval = 0)
    gradient = np.arctan2(gradient_y,gradient_x)
    
    if debug_show_gradient:
        pixels = pygame.surfarray.pixels2d(gradient_surface)
        pixel_alphas = pygame.surfarray.pixels_alpha(gradient_surface)
        c = np.zeros_like(gradient)
        c[gradient > 0] = (255 * gradient[gradient > 0] * math.pi).astype(int) << 16
        c[gradient < 0] = (255 * gradient[gradient < 0] * -math.pi).astype(int)
        temp = np.repeat(c, CELL_SIZE, axis=0)
        pixels[:] = np.repeat(temp, CELL_SIZE, axis=1)
        pixel_alphas.fill(0)
        pixel_alphas[pixels != 0] = 100

        del pixels
        del pixel_alphas

def draw_ants():
    global ants
    pixels = pygame.surfarray.pixels2d(ant_surface)
    pixel_alphas = pygame.surfarray.pixels_alpha(ant_surface)
    pixels.fill(0)
    pixel_alphas.fill(0)
    for i,j in ants['pos']:
        x, y = int(i), int(j)
        pixels[x,y] = 16777215
        pixel_alphas[x,y] = 255
    del pixels
    del pixel_alphas

run = True
while (run):

    delta_time = min(MAX_ELAPSED_TIME, time.time() - prev_time)
    prev_time = time.time()
    screen.fill((0,0,0))

    if debug_timed_run:
        debug_timed_run_timer -= delta_time
        if debug_timed_run_timer <= 0:
            run = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            match e.key:
                case pygame.K_g:
                    debug_show_grid = not debug_show_grid
            match e.key:
                case pygame.K_v:
                    debug_show_gradient = not debug_show_gradient
            match e.key:
                case pygame.K_p:
                    debug_show_pheromones = not debug_show_pheromones
    pheromone_timer -= delta_time
    update_ant_pos(delta_time)
    while pheromone_timer <= 0:
        pheromone_timer += PHEROMONE_UPDATE_SPEED
        ants_drop_pheromones()
        update_pheromones()
    gradient_timer -= delta_time
    while gradient_timer <= 0:
        update_gradient()
        gradient_timer += GRADIENT_UPDATE_SPEED
    draw_ants()
    


    if debug_show_grid:
        screen.blit(grid_surface, (0,0))
    if debug_show_gradient:
        screen.blit(gradient_surface, (0,0))
    if debug_show_pheromones:
        screen.blit(pheromone_surface, (0,0))
    screen.blit(wall_surface, (0,0))
    screen.blit(ant_surface, (0,0))
    if debug_show_gradient:
        screen.blit(gradient_surface, (0,0))

    pygame.display.update()

pygame.quit()