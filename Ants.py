import pygame, math, random, time, tools

WINDOW = (1200, 750)

pygame.init()

#TODO Solve collisions with corners sometimes allowing passage

screen = pygame.display.set_mode(WINDOW)
surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
font = pygame.font.Font(None, 20)


run = True
fps = 0
grid_cell_size = 25
x_grid = int(WINDOW[0] / grid_cell_size)
y_grid = int(WINDOW[1] / grid_cell_size)

prev_time = time.time()
dt = time.time()

#Debuggers
debug_collisions = False
debug_ant_sight = True
debug_pheromones = True
debug_wall_outlines = False
show_fps = True
transparent_walls = True
debug_grid = True

class grid_cell:
    def __init__(self, pos, size, index):
        self.pos = pos
        self.size = size
        self.index = index
        self.pings = 0

grid_cells = []
for i in range(x_grid):
    row = []
    for j in range(y_grid):
        row.append(grid_cell((i*grid_cell_size, j*grid_cell_size), grid_cell_size, (i, j)))
    grid_cells.append(row)

class wall:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

window_borders = [((0, 0), (WINDOW[0], 10)), ((0, 0), (10, WINDOW[1])), ((0, WINDOW[1] - 10), (WINDOW[0], 10)), ((WINDOW[0] - 10, 0), (10, WINDOW[1]))]
wall_coordinates = [((500, 500), (80, 10)), ((490, 310), (10, 80)), ((690, 310), (10, 80)), ((500, 300), (80, 10)), ((490, 420), (10, 80)), ((690, 420), (10, 80)), ((610, 300), (80, 10)), ((610, 500), (80, 10))]
wall_coordinates += window_borders
walls = []

for c in wall_coordinates:
    walls.append(wall(c[0],c[1]))

class pheromone:
    def __init__(self, pos, type, color, strength, size):
        self.pos = pos
        self.type = type
        self.color = color
        self.strength = strength
        self.size = size
        self.index = (math.floor(self.pos[0] / grid_cell_size), math.floor(self.pos[1] / grid_cell_size))
    def update(self, dt):
        self.strength -= .1 * dt
        self.color = (self.color[0], self.color[1], self.color[2], 150 * self.strength if self.strength > 0 else 0)
        self.draw(self.color, self.pos, self.size)
        if self.strength < 0:
            pheromones.remove(self)
    def draw(self, color, pos, size):
        if not debug_pheromones:
            return
        pygame.draw.circle(surface, color, pos, size)
        
            

pheromones = []

class ant:
    def __init__(self, pos, color, angle, speed, size):
        self.pos = pos
        self.color = color
        self.angle = angle
        self.speed = speed
        self.size = size
        self.poly = [(0,1),(1,1),(2,2),(3,1),(4,2),(3,3),(2,2),(1,3),(0,3)]
        self.pheromone_clock = random.random() * 1
        self.pheromone_reset = 1
        self.found_pheromones = (0, 0, 0) #each of the 5 raycasts
    def look(self):
        center = (self.pos[0] + .5 * self.size, self.pos[1] + .5 * self.size)
        viewpoint = (center[0] + self.size * .5 + 2*math.cos(self.angle), center[1] + self.size * .5 + 2*math.sin(self.angle))
        self.found_pheromones = [0,0,0]
        m = 0
        for i in range(-30, 31, 30):
            endpoint = (viewpoint[0] + 30*math.cos(self.angle + math.pi * (1/180) * i), viewpoint[1] + 30*math.sin(self.angle + math.pi * (1/180) * i))
            pos_index = (int(self.pos[0] / grid_cell_size), int(self.pos[1] / grid_cell_size))
            
            for p in pheromones:
                x_dir = tools.sign(math.cos(self.angle))
                y_dir = tools.sign(math.sin(self.angle))
                p1 = p.index
                p2 = (p.index[0] + x_dir, p.index[1] + y_dir)
                if (p1 != pos_index) and (p1 != (p2[0], p1[1])) and (p1 != (p1[0], p2[1])) and (p1 != (p2[0], p2[1])):
                    continue
                if (debug_grid):
                    if p1[0] > 0 and p1[0] < x_grid and p1[1] > 0 and p1[1] < y_grid:
                        if (p.index == pos_index): grid_cells[p1[0]][p1[1]].pings += 1
                    if p2[0] > 0 and p2[0] < x_grid and p1[1] > 0 and p1[1] < y_grid:
                        if (p.index == p2[0], p1[1]): grid_cells[p2[0]][p1[1]].pings += 1
                    if p1[0] > 0 and p1[0] < x_grid and p2[1] > 0 and p2[1] < y_grid:
                        if (p.index == p1[0], p2[1]): grid_cells[p1[0]][p2[1]].pings += 1
                    if p2[0] > 0 and p2[0] < x_grid and p2[1] > 0 and p2[1] < y_grid:
                        if (p.index == p2[0], p2[1]): grid_cells[p2[0]][p2[1]].pings += 1

                if (tools.line_circle_intersection(p.size, p.pos, viewpoint, endpoint)):
                    self.found_pheromones[m] += p.strength
            if debug_ant_sight:
                pygame.draw.line(surface, (255, 255, 255, 50), viewpoint, endpoint, 1)
            m += 1
    def explore(self):
        max_pheromones = 0
        max_index = -1
        for i in range(self.found_pheromones.__len__()):
            if self.found_pheromones[i] > max_pheromones:
                max_pheromones = self.found_pheromones[i]
                max_index = i
        match max_index:
            case 0:
                self.angle = self.angle - dt * speed * .5
            case 1:
                pass
            case 2:
                self.angle = self.angle + dt * speed * .5
        self.angle = self.angle + (random.random() * 2 - 1) * dt * speed * .25
        x_movement = math.cos(self.angle) * dt * speed
        y_movement = math.sin(self.angle) * dt * speed
        new_x = self.pos[0] + x_movement
        new_y = self.pos[1] + y_movement
        bound = (self.pos[0], self.pos[1])
        if (x_movement > 0): bound = (bound[0] + self.size, bound[1])
        else : bound = (bound[0], bound[1])
        if (y_movement > 0): bound = (bound[0], bound[1] + self.size)
        else : bound = (bound[0], bound[1])
        for w in walls:
            p1 = w.pos
            p2 = (w.pos[0] + w.size[0], w.pos[1])
            p3 = (w.pos[0] + w.size[0], w.pos[1] + w.size[1])
            p4 = (w.pos[0], w.pos[1] + w.size[1])
            for p in [(p1,p2), (p2,p3), (p3,p4), (p4,p1)]:
                if tools.line_line_intersection(bound, (new_x, bound[1]), p[0], p[1]):
                    new_x = self.pos[0]
                    if debug_collisions:
                        pygame.draw.line(screen, (255,0,255), bound, (new_x + 100*x_movement, new_y + 100*y_movement), 1)
                if tools.line_line_intersection(bound, (bound[0], new_y), p[0], p[1]):
                    new_y = self.pos[1]
                    if debug_collisions:
                        pygame.draw.line(screen, (255,0,255), bound, (new_x + 100*x_movement, new_y + 100*y_movement), 1)

        self.pos = (new_x, new_y)
    def pheromones(self, dt):
        self.pheromone_clock -= dt
        if self.pheromone_clock < 0:
            self.pheromone_clock = self.pheromone_reset
            pheromones.append(pheromone(self.pos, 1, (0,0,255,200), 1, 2))

ants = []

for i in range (60):
    pos = (600, 400)
    color = (random.randint(50, 205), random.randint(50, 205), random.randint(50, 205))
    angle = (random.random() * math.pi * 2)
    speed = 50
    size = 4
    ants.append(ant(pos, color, angle, 20, 4))

while run:
    screen.fill((0, 0, 0))
    surface.fill((0,0,0,0))
    dt = time.time() - prev_time
    if (show_fps):
        if dt != 0:
            fps = int(1 / dt)
        text_surface = font.render("fps: " + str(fps) + " pheromones: " + str(pheromones.__len__()) + " ants: " + str(ants.__len__()), True, (155,155,155))
        screen.blit(text_surface, (15,15))
    prev_time = time.time()

    for p in pheromones:
        p.update(dt)

    for a in ants:
        a.look()
        a.explore()
        a.pheromones(dt)
        tools.draw_angled_poly(screen, a.poly, a.pos, a.color, a.angle)

    for w in walls:
        if (debug_wall_outlines):
            p1 = w.pos
            p2 = (w.pos[0] + w.size[0], w.pos[1])
            p3 = (w.pos[0] + w.size[0], w.pos[1] + w.size[1])
            p4 = (w.pos[0], w.pos[1] + w.size[1])
            for p in [(p1, p2), (p2, p3), (p3, p4), (p4, p1)]:
                pygame.draw.line(surface, (200, 0, 0), p[0], p[1])
        else:
            pygame.draw.rect(surface, (155,155,155,100 if transparent_walls else 255), (w.pos, w.size))

    if (debug_grid):
        for gc_row in grid_cells:
            for gc in gc_row:
                blue = 0 if gc.pings == 0 else 255
                p1 = gc.pos
                p2 = (gc.pos[0] + gc.size - 1, gc.pos[1] + gc.size - 1)
                pygame.draw.line(surface, (0, 0, blue, 100), p1, (p2[0], p1[1]))
                pygame.draw.line(surface, (0, 0, blue, 100), p1, (p1[0], p2[1]))
                pygame.draw.line(surface, (0, 0, blue, 100), (p1[0], p2[1]), (p2[0], p2[1]))
                pygame.draw.line(surface, (0, 0, blue, 100), (p2[0], p1[1]), (p2[0], p2[1]))

                gc.pings = 0

    screen.blit(surface, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

