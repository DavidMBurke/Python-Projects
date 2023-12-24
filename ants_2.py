import pygame, math, numpy as np, time, random


WINDOW = (1200, 800)

#Display surfaces
SCREEN = pygame.display.set_mode(WINDOW)
GRID_SURFACE = pygame.Surface((WINDOW), pygame.SRCALPHA)
WALL_SURFACE = pygame.Surface((WINDOW), pygame.SRCALPHA)
PHEROMONE_SURFACE = pygame.Surface((WINDOW), pygame.SRCALPHA)
ANT_SURFACE = pygame.Surface((WINDOW), pygame.SRCALPHA)

CELL_SIZE = 5
CELL_ROWS = WINDOW[1] // CELL_SIZE
CELL_COLS = WINDOW[0] // CELL_SIZE
NUM_ANTS = 1000
PHEROMONE_TIME = 0.5
ANT_SPEED = 20
PHEROMONE_UPDATE_SPEED = .1 #time in seconds to decrease pheromones on a square
PHEROMONE_DECREASE_AMOUNT = 1 #amount of decrease per update
PHEROMONE_STRENGTH = 10

pheromone_timer = PHEROMONE_UPDATE_SPEED # time until pheromone disappates by 1
prev_time = time.time()
delta_time = time.time()
pygame.init()

#Debug Settings
debug_show_grid = False # g key
timed_run = True # For profiling
timed_run_timer = 30.0 # For profiling

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
    pygame.draw.line(GRID_SURFACE, (100,100,100), (i, 0), (i, CELL_ROWS * CELL_SIZE))
for j in range (0, WINDOW[1], CELL_SIZE):
    pygame.draw.line(GRID_SURFACE, (100,100,100), (0, j), (CELL_COLS * CELL_SIZE, j))

#Set walls
grid_cells[:, 0]['wall'] = True
grid_cells[:, CELL_ROWS-1]['wall'] = True
grid_cells[0, :]['wall'] = True
grid_cells[CELL_COLS - 1, :]['wall'] = True

#Draw walls
for (x,y), cell in np.ndenumerate(grid_cells):
    if cell['wall']:
        pygame.draw.rect(WALL_SURFACE, (100, 100, 100), (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))


ant_dtype = np.dtype([
    ('pos', float, (2,)),
    ('index', int, (2,)),
    ('direction', float)
])

#Initialize ants
ants = np.zeros(NUM_ANTS, dtype = ant_dtype)
for i in range(NUM_ANTS):
    pos = (600,400)
    index = (pos[0] // CELL_SIZE, pos[1] // CELL_SIZE)
    direction = (random.random() * 2 * math.pi)
    ants[i] = (pos, index, direction)

def update_ant_pos(delta_time):
    rand_array = (np.random.rand(ants['direction'].shape[0]) * 2 - 1)
    ants['direction'] += rand_array * delta_time * 10
    x = np.cos(ants['direction']) * delta_time * ANT_SPEED
    y = np.sin(ants['direction']) * delta_time * ANT_SPEED
    movement = np.column_stack((x,y))
    ants['pos'] += movement
    ants['index'] = np.floor(ants['pos'] / CELL_SIZE).astype(int)

def ants_drop_pheromones():
    for i, j in ants['index']:
        grid_cells[i, j]['pheromones'][0] += PHEROMONE_STRENGTH
    
def update_pheromones():
    grid_cells['pheromones'] = np.clip(grid_cells['pheromones'] - PHEROMONE_DECREASE_AMOUNT, 0, 255)
    for index, c in np.ndenumerate(grid_cells):
        pygame.draw.rect(PHEROMONE_SURFACE, c['pheromones'], (c['pos'][0], c['pos'][1], CELL_SIZE, CELL_SIZE))


def draw_ants():
    global ants
    pixels = pygame.surfarray.pixels2d(ANT_SURFACE)
    pixel_alphas = pygame.surfarray.pixels_alpha(ANT_SURFACE)
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

    delta_time = time.time() - prev_time
    prev_time = time.time()
    SCREEN.fill((0,0,0))

    if (timed_run):
        timed_run_timer -= delta_time
        if timed_run_timer <= 0:
            run = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            match e.key:
                case pygame.K_g:
                    debug_show_grid = not debug_show_grid
    pheromone_timer -= delta_time
    update_ant_pos(delta_time)
    while pheromone_timer <= 0:
        pheromone_timer += PHEROMONE_UPDATE_SPEED
        ants_drop_pheromones()
        update_pheromones()
    draw_ants()
    


    if debug_show_grid:
        SCREEN.blit(GRID_SURFACE, (0,0))
    SCREEN.blit(WALL_SURFACE, (0,0))
    SCREEN.blit(PHEROMONE_SURFACE, (0,0))
    SCREEN.blit(ANT_SURFACE, (0,0))

    pygame.display.update()

pygame.quit()