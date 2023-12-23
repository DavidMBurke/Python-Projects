import pygame, random, math, time, numpy as np, pygame.surfarray as surfarray

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SQUARE_SIZE = 5
PARTICLE_DISTRIBUTION = 3
DENSITY_CORRECTION = 4 #How rapidly particles move from high to low density
SURROUNDING_FLOW_FACTOR = 3 # How much weight surrounding flow has vs. current flow of a square
CURRENT_FLOW_FACTOR = 5
FLOW_NORMALIZE_FACTOR = 1 / (SURROUNDING_FLOW_FACTOR + CURRENT_FLOW_FACTOR)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
particle_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
prev_time = time.time()
prev_mouse_pos = (0, 0)
mouse_angle = 0
ROWS = int(SCREEN_WIDTH / SQUARE_SIZE)
COLS = int(SCREEN_HEIGHT / SQUARE_SIZE)
test_value = 0
num_particles = int(SCREEN_WIDTH * SCREEN_HEIGHT / (PARTICLE_DISTRIBUTION**2))
font = pygame.font.Font(None, 20)


show_fps = True
refresh_each_frame = True
pump_speed = 0
gravity_mode = False #Has no value to simulation, just a cool bug I found

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
    b = 255 - (r + g) // 2
    particles[i]['position'] = [x, y]
    particles[i]['color'] = r + 255 * g + 255 * 255 * b

#Reset colors
def reset_colors():
    for i in range(num_particles):
        [x, y] = particles[i]['position']
        r = 255 * x / SCREEN_WIDTH
        g = 255 * y / SCREEN_HEIGHT
        b = 255 - (r + g) // 2
        particles[i]['color'] = r + 255 * g + 255 * 255 * b

#Initialize squares
squares = np.zeros((ROWS,COLS), dtype = square_dtype)
for i in range(ROWS):
    for j in range(COLS):
        pos = (i * SQUARE_SIZE, j * SQUARE_SIZE)
        place = (i, j)
        flow = (random.random() * 2 - 1, random.random() * 2 - 1)
        squares[i, j] = (place, pos, SQUARE_SIZE, flow, 0)

run = True
q = 0

def add_pumps():
    if pump_speed == 0:
        return
    for i in range (ROWS):
        for j in range (int(COLS * 0), int(COLS * .05)):
            squares[i, j]['flow'] = (-pump_speed, squares[i, j]['flow'][1])

    for i in range (ROWS):
        for j in range (int(COLS * 0.5), int(COLS * .55)):
            squares[i, j]['flow'] = (pump_speed, squares[i, j]['flow'][1])

    for i in range (int(ROWS * 0), int(ROWS * .05)):
        for j in range (COLS):
            squares[i, j]['flow'] = (squares[i, j]['flow'][0], -pump_speed)

    for i in range (int(ROWS * .5), int(ROWS * .55)):
        for j in range (COLS):
            squares[i, j]['flow'] = (squares[i, j]['flow'][0], pump_speed)

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

    flow_x_sum /= 4
    flow_y_sum /= 4

    #average the flow at a 6/4 ratio of current and surrounding ave
    next_flow_x = (flow_x_sum * SURROUNDING_FLOW_FACTOR + squares['flow'][:,:,0] * CURRENT_FLOW_FACTOR + density_gradient_x * DENSITY_CORRECTION * delta_time * (-1 if gravity_mode else 1)) * FLOW_NORMALIZE_FACTOR
    next_flow_y = (flow_y_sum * SURROUNDING_FLOW_FACTOR + squares['flow'][:,:,1] * CURRENT_FLOW_FACTOR + density_gradient_y * DENSITY_CORRECTION * delta_time * (-1 if gravity_mode else 1)) * FLOW_NORMALIZE_FACTOR

    #update flow
    squares['flow'] = np.stack((next_flow_x, next_flow_y), axis = -1)

def update_particles():
    global squares

    squares['density'] = 0

    #Wrap boundaries
    positions = particles['position'] 
    positions %= [SQUARE_SIZE * ROWS, SQUARE_SIZE * COLS]

    #Find grid indices for flow lookup
    grid_x = np.clip(np.floor(positions[:, 0] / SQUARE_SIZE).astype(int), 0, ROWS - 1)
    grid_y = np.clip(np.floor(positions[:, 1] / SQUARE_SIZE).astype(int), 0, COLS - 1)
    flows = squares[grid_x, grid_y]['flow']

    #Update positions
    np.add(positions, flows * 100 * delta_time, out = positions)

    #Update density
    np.add.at(squares['density'], (grid_x, grid_y), 1)

    #get pixels as np array (locks particle_surface)
    pixels = surfarray.pixels2d(particle_surface)
    if (refresh_each_frame):
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
    mouse_pos = pygame.mouse.get_pos()
    if mouse_pos != prev_mouse_pos:
        mouse_angle = math.atan2((mouse_pos[1] - prev_mouse_pos[1]), (mouse_pos[0] - prev_mouse_pos[0]))
        prev_mouse_pos = pygame.mouse.get_pos()

    if (show_fps):
        if delta_time != 0:
            fps = int(1 / delta_time)
        text_surface = font.render("fps: " + str(fps) + " particles: " + str(num_particles), True, (155,155,155))
        screen.blit(text_surface, (15,15))
    prev_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_r:
                    refresh_each_frame = not refresh_each_frame
                case pygame.K_t:
                    reset_colors()
                case pygame.K_g:
                    gravity_mode = not gravity_mode
                case pygame.K_0:
                    pump_speed = 0
                case pygame.K_1:
                    pump_speed = 1
                case pygame.K_2:
                    pump_speed = 2
                case pygame.K_3:
                    pump_speed = 3
                case pygame.K_4:
                    pump_speed = 4
                case pygame.K_5:
                    pump_speed = 5
    if pygame.mouse.get_pressed()[0]:
        mouse_index = (mouse_pos[0] // SQUARE_SIZE, mouse_pos[1] // SQUARE_SIZE)
        flow_dir = (math.cos(mouse_angle), math.sin(mouse_angle))
        for i in range(-1,1):
            for j in range (-1,1):
                xi = (mouse_index[0] + i) % COLS
                yj = (mouse_index[1] + j) % ROWS
                squares[xi,yj]['flow'] = [5 * flow_dir[0], 5 * flow_dir[1]]

    add_pumps()

    update_squares()

    update_particles()

    screen.blit(particle_surface, (0,0))
    pygame.display.update()

pygame.quit()

