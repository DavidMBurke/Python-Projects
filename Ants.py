import pygame, math, random, time, tools

WINDOW = (1200, 750)

pygame.init()

screen = pygame.display.set_mode(WINDOW)
surface = pygame.Surface((WINDOW), pygame.SRCALPHA)
font = pygame.font.Font(None, 20)

run = True
fps = 0

prev_time = time.time()
delta_time = time.time()

#Debuggers
debug_collisions = False
debug_ant_sight = True
show_fps = True

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

class ant:
    def __init__(self, pos, color, angle, speed, size):
        self.pos = pos
        self.color = color
        self.angle = angle
        self.speed = speed
        self.size = size
        self.poly = [(0,1),(1,1),(2,2),(3,1),(4,2),(3,3),(2,2),(1,3),(0,3)]
    def look(self):
        center = (self.pos[0] + .5 * self.size, self.pos[1] + .5 * self.size)
        viewpoint = (center[0] + self.size * .5 + 2*math.cos(self.angle), center[1] + self.size * .5 + 2*math.sin(self.angle))
        if debug_ant_sight:
            for i in range(-50, 51, 25):
                endpoint = (viewpoint[0] + 30*math.cos(self.angle + math.pi * (1/180) * i), viewpoint[1] + 30*math.sin(self.angle + math.pi * (1/180) * i))
                pygame.draw.line(surface, (255, 255, 255, 50), viewpoint, endpoint, 1)
    def explore(self):
        self.angle = self.angle + (random.random() * 2 - 1) * delta_time * speed * .5
        x_movement = math.cos(self.angle) * delta_time * speed
        y_movement = math.sin(self.angle) * delta_time * speed
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
                if tools.check_line_intersection(bound, (new_x, bound[1]), p[0], p[1]):
                    new_x = self.pos[0]
                    if debug_collisions:
                        pygame.draw.line(screen, (255,0,255), bound, (new_x + 100*x_movement, new_y + 100*y_movement), 1)
                if tools.check_line_intersection(bound, (bound[0], new_y), p[0], p[1]):
                    new_y = self.pos[1]
                    if debug_collisions:
                        pygame.draw.line(screen, (255,0,255), bound, (new_x + 100*x_movement, new_y + 100*y_movement), 1)

        self.pos = (new_x, new_y)

ants = []

for i in range (500):
    pos = (600, 400)
    color = (random.randint(50, 205), random.randint(50, 205), random.randint(50, 205))
    angle = (random.random() * math.pi * 2)
    speed = 50
    size = 4
    ants.append(ant(pos, color, angle, 20, 4))

print(tools.check_line_intersection((0, 0), (20, 20), (10, 10), (30, 30))) # True
print(tools.check_line_intersection((0, 0), (10, 10), (10, 10), (20, 20))) # True


# print(tools.check_line_intersection((0, 0), (20, 20), (10, 10), (30, 30))) # True
# print(tools.check_line_intersection((0, 0), (20, 20), (10, 10), (10, 0))) # True
# print(tools.check_line_intersection((0, 0), (20, 20), (0, 1), (20, 21))) # False
# print(tools.check_line_intersection((0, 0), (10, 10), (10, 10), (20, 20))) # True
# print(tools.check_line_intersection((0, 0), (10, 10), (10, 10), (20, 0))) # True
# print(tools.check_line_intersection((0, 0), (10, 10), (12, 12), (20, 20))) # False
# print(tools.check_line_intersection((0, 0), (10, 10), (20, 20), (30, 30))) # False
# print(tools.check_line_intersection((0, 10), (20, 10), (10, 0), (10, 20))) # True
# print(tools.check_line_intersection((0, 0), (10, 10), (10, 10), (20, 10))) # True
# print(tools.check_line_intersection((0, 0), (20, 20), (0, 20), (20, 0))) # True



while run:
    screen.fill((0, 0, 0))
    surface.fill((0,0,0,0))
    delta_time = time.time() - prev_time
    if (show_fps):
        if delta_time != 0:
            fps = 1 / delta_time
        text_surface = font.render(str(fps), True, (155,155,155))
        screen.blit(text_surface, (15,15))
    prev_time = time.time()

    for a in ants:
        a.explore()
        a.look()
        tools.draw_angled_poly(screen, a.poly, a.pos, a.color, a.angle, 4)

    for w in walls:
        pygame.draw.rect(surface, (155,155,155,100), (w.pos, w.size))


    screen.blit(surface, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

