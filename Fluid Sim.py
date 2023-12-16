import pygame, random, math, time, numpy as np

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SIZE = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
prev_time = time.time()
ROWS = int(SCREEN_WIDTH / SIZE)
COLS = int(SCREEN_HEIGHT / SIZE)
prev_pos = (0,0)
adjacent_positions = [(0,1),(1,0),(0,-1),(-1,0)]
test_value = 0

class mapSquare:
    def __init__(self, place, pos, size, flow):
        self.place = place
        self.pos = pos
        self.size = size
        self.flow = flow

class particle:
    def __init__(self, pos):
        self.pos = (float(pos[0]), float(pos[1]))
        self.color = (255 * pos[0] / SCREEN_WIDTH, 100, 255 * pos[1] / SCREEN_HEIGHT)

def draw_gradient_circle(screen, x, y, radius, color):
    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for dy in range(-radius,radius):
        for dx in range(-radius, radius):
            distance = math.sqrt(dx**2 + dy**2)
            if distance < radius:
                alpha = 255 - int((distance**2 / radius **2) * 255)
                gradient_color = (*color[:3], alpha)
                circle_surface.set_at((dx + radius, dy + radius), gradient_color)
    screen.blit(circle_surface, (x - radius, y - radius))

squares = []
next_squares = []
particles = []
for i in range(ROWS):
    for j in range (COLS):
        pos = (i * SIZE, j * SIZE)
        place = (i, j)
        flow = (random.random() * 2 - 1, random.random() * 2 - 1)
        squares.append(mapSquare(place, pos, SIZE, flow))
        next_squares.append(mapSquare(place, pos, SIZE, flow))

for i in range(SCREEN_WIDTH):
    for j in range(SCREEN_HEIGHT):
        if i % 5 == 3 and j % 5 == 0: 
            particles.append(particle((float(i),float(j))))
        

run = True
q = 0
while run:
    delta_time = time.time() - prev_time
    prev_time = time.time()
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range (int(COLS * 0), int(COLS * .03)):
        for j in range (ROWS):
            squares[i*COLS+j].flow = (squares[i*COLS+j].flow[0], -1)

    for i in range (ROWS):
        for j in range (int(COLS * 0), int(COLS * .03)):
            squares[i*COLS+j].flow = (-1, squares[i*COLS+j].flow[1])

    for i in range (int(COLS * .5), int(COLS * .53)):
        for j in range (ROWS):
            squares[i*COLS+j].flow = (squares[i*COLS+j].flow[0], 1)

    # for i in range (ROWS):
    #     for j in range (int(COLS * .5), int(COLS * .53)):
    #         squares[i*COLS+j].flow = (1, squares[i*COLS+j].flow[1])

    for square in squares:
        x = square.pos[0]
        y = square.pos[1]
        arrow_polygon = ((x + 1, y + 4), (x + 1, y + 6), (x + 6, y + 6), (x + 6, y + 8), (x + 9, y + 5), (x + 6, y + 2), (x + 6, y + 4))
        

        # x_0 = square.place[0]
        # y_0 = square.place[1]
        # arrow_with_direction = []
        # x_m1 = int(x_0 - 1)
        # x_p1 = int(x_0 + 1)
        # y_m1 = int(y_0 - 1)
        # y_p1 = int(y_0 + 1)
        # if x_m1 == -1: x_m1 = ROWS - 1
        # if x_p1 == ROWS : x_p1 = 0
        # if y_m1 == -1: y_m1 = COLS - 1
        # if y_p1 == COLS : y_p1 = 0
        # term1 = np.dot(np.array(squares[x_m1 * COLS + y_m1].flow) + np.array(squares[x_p1 * COLS + y_p1].flow), [1,1])
        # term2 = np.dot(np.array(squares[x_m1 * COLS + y_p1].flow) + np.array(squares[x_p1 * COLS + y_m1].flow), [1, -1]) * np.array((1, -1))
        # term3 = (np.array(squares[x_m1 * COLS + y_0].flow) + np.array(squares[x_p1 * COLS + y_0].flow) - np.array(squares[x_0 * COLS + y_m1].flow) - np.array(squares[x_0 * COLS + y_p1].flow)) * np.array((2,-2))
        # term4 = np.array(square.flow) * -4
        # next_squares[x_0 * COLS + y_0].flow = np.array(square.flow) + (term1 + term2 + term3 + term4) * (1/8)
       
        flow_x_sum = 0
        flow_y_sum = 0
        for i, j in adjacent_positions:
            m = square.place[0] + i
            n = square.place[1] + j
            if m == -1: m = ROWS - 1
            if n == -1: n = COLS - 1
            if m == ROWS : m = 0
            if n == COLS : n = 0
            index = int(m * COLS + n)
            flow_x_sum += squares[index].flow[0]
            flow_y_sum += squares[index].flow[1]
        flow_x = (flow_x_sum + square.flow[0] * 6) * .1
        flow_y = (flow_y_sum + square.flow[1] * 6) * .1
        square.flow = (flow_x, flow_y)
        if square.place[0] % 2 == 0 or square.place[1] % 2 == 0:
            continue
        continue
        flow_angle = math.atan2(square.flow[1], square.flow[0])
        s = math.sin(flow_angle)
        c = math.cos(flow_angle)
        for point in arrow_polygon:
            x_rotation_axis = square.pos[0] + .5 * square.size
            y_rotation_axis = square.pos[1] + .5 * square.size
            x_about_origin = point[0] - x_rotation_axis
            y_about_origin = point[1] - y_rotation_axis
            x_new = x_about_origin * c - y_about_origin * s
            y_new = x_about_origin * s + y_about_origin * c
            x_f = x_new + x_rotation_axis
            y_f = y_new + y_rotation_axis
            arrow_with_direction.append((x_f, y_f))
        magnitude = math.sqrt(square.flow[0] * square.flow[0] + square.flow[1] * square.flow[1])
        if magnitude > 1: magnitude = 1
        pygame.draw.polygon(screen, (255 * magnitude, 0, 255 - (255 * magnitude)), arrow_with_direction)
        pygame.draw.polygon(screen, (255 * magnitude, 0, 255 - (255 * magnitude)), arrow_with_direction)
    squares = next_squares[:]
    for p in particles:
        new_x = p.pos[0]
        new_y = p.pos[1]
        if p.pos[0] >= SIZE * ROWS: new_x -= SIZE * ROWS
        if p.pos[1] >= SIZE * COLS: new_y -= SIZE * COLS
        if p.pos[0] < 0: new_x += SIZE * ROWS
        if p.pos[1] < 0: new_y += SIZE * COLS
        x = int(new_x / SIZE)
        y = int(new_y / SIZE)
        flow = squares[x * COLS + y].flow
        new_x += flow[0] * 100 * delta_time
        new_y += flow[1] * 100 * delta_time
        p.pos = (new_x, new_y)
        pygame.draw.circle(screen, p.color, p.pos, 1)
        #        draw_gradient_circle(screen, p.pos, 3, p.color)
    pygame.display.update()

pygame.quit()