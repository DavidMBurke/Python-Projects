import pygame, random, math, time, numpy as np, pygame.surfarray as surfarray

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SIZE = 5
PARTICLE_DISTRIBUTION = 5
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
particle_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
prev_time = time.time()
ROWS = int(SCREEN_WIDTH / SIZE)
COLS = int(SCREEN_HEIGHT / SIZE)
prev_pos = (0,0)
test_value = 0
num_particles = int(SCREEN_WIDTH * SCREEN_HEIGHT / (PARTICLE_DISTRIBUTION**2))
font = pygame.font.Font(None, 20)


show_fps = True

square_dtype = np.dtype([
    ('place', int, (2,)),
    ('pos', int, (2,)),
    ('size', int),
    ('flow', float, (2,)),
    ('density', int) 
])

particle_dtype = np.dtype([
    ('position', float, (2,)),
    ('color', int)
])

#Initialize particles
particles = np.zeros(num_particles, dtype = particle_dtype)
for i in range(num_particles):
    x = (i % (SCREEN_WIDTH // PARTICLE_DISTRIBUTION)) * PARTICLE_DISTRIBUTION        
    y = (i // (SCREEN_WIDTH // PARTICLE_DISTRIBUTION)) * PARTICLE_DISTRIBUTION
    r = 255 * x / SCREEN_WIDTH
    g = 255 * y / SCREEN_HEIGHT
    b = 255
    particles[i]['position'] = [x, y]
    particles[i]['color'] = r + 255 * g + 255 * 255 * b

#Initialize squares
squares = np.zeros((ROWS,COLS), dtype = square_dtype)
for i in range(ROWS):
    for j in range(COLS):
        pos = (i * SIZE, j * SIZE)
        place = (i, j)
        flow = (random.random() * 2 - 1, random.random() * 2 - 1)
        squares[i, j] = (place, pos, SIZE, flow, 0)

run = True
q = 0

def draw_flowpaths():
    for i in range (ROWS):
        for j in range (int(COLS * 0), int(COLS * .03)):
            squares[i, j]['flow'] = (-1, squares[i, j]['flow'][1])

    for i in range (ROWS):
        for j in range (int(COLS * 0.5), int(COLS * .53)):
            squares[i, j]['flow'] = (1, squares[i, j]['flow'][1])

    for i in range (int(ROWS * 0), int(ROWS * .03)):
        for j in range (COLS):
            squares[i, j]['flow'] = (squares[i, j]['flow'][0], -1)

    for i in range (int(ROWS * .5), int(ROWS * .53)):
        for j in range (COLS):
            squares[i, j]['flow'] = (squares[i, j]['flow'][0], 1)

def update_squares():
    adjacent_positions = [(0,1),(1,0),(0,-1),(-1,0)]
    global squares  # Ensure we modify the global squares array

    flow_x_sum = np.zeros((ROWS, COLS))
    flow_y_sum = np.zeros((ROWS, COLS))
    density_gradient_x = np.zeros((ROWS, COLS))
    density_gradient_y = np.zeros((ROWS, COLS))

    #shift array in each direction and sum new values
    for di, dj in adjacent_positions:
        shifted_squares = np.roll(squares, shift=(di,dj), axis=(0,1))
        #Sum adjacent flows
        flow_x_sum += shifted_squares['flow'][:,:,0]
        flow_y_sum += shifted_squares['flow'][:,:,1]
        #Calculate density gradients
        density_diff = shifted_squares['density'] - squares['density']
        density_gradient_x += di * density_diff
        density_gradient_y += dj * density_diff

    #average the flow at a 6/4 ratio of current and surrounding ave
    next_flow_x = (flow_x_sum + squares['flow'][:,:,0] * 6 + density_gradient_x * .1) * 0.1
    next_flow_y = (flow_y_sum + squares['flow'][:,:,1] * 6 + density_gradient_y * .1) * 0.1

    #update flow
    squares['flow'] = np.stack((next_flow_x, next_flow_y), axis = -1)

def update_particles():
    global squares

    squares['density'] = 0

    #Wrap boundaries
    positions = particles['position'] 
    densities = squares['density']
    positions %= [SIZE * ROWS, SIZE * COLS]

    #Find grid indices for flow lookup
    grid_x = np.clip(np.floor(positions[:, 0] / SIZE).astype(int), 0, ROWS - 1)
    grid_y = np.clip(np.floor(positions[:, 1] / SIZE).astype(int), 0, COLS - 1)
    flows = squares[grid_x, grid_y]['flow']

    #Update positions
    np.add(positions, flows * 100 * delta_time, out = positions)

    #Update density
    np.add.at(squares['density'], (grid_x, grid_y), 1)

    #get pixels as np array (locks particle_surface)
    pixels = surfarray.pixels2d(particle_surface)
    pixels.fill(0)

    #color pixels at particle positions
    screen_positions = np.clip(positions.astype(int), [0, 0], [SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1])
    for pos, color in zip(screen_positions, particles['color']):
        pixels[tuple(pos)] = color

    # release surface lock
    del pixels


while run:
    delta_time = time.time() - prev_time
    prev_time = time.time()

    #screen.fill((0,0,0))

    if (show_fps):
        if delta_time != 0:
            fps = int(1 / delta_time)
        text_surface = font.render("fps: " + str(fps) + " particles: " + str(num_particles), True, (155,155,155))
        screen.blit(text_surface, (15,15))
    prev_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_flowpaths()

    update_squares()

    update_particles()

    screen.blit(particle_surface, (0,0))
    pygame.display.update()

pygame.quit()

