import pygame, math, random, time

WINDOW = (1200, 800)


screen = pygame.display.set_mode(WINDOW)
surface = pygame.Surface((WINDOW), pygame.SRCALPHA)

run = True

prev_time = time.time()
delta_time = time.time()

def rotate_polygon(polygon, axis, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    rotated_poly = []
    for point in polygon:
        x_about_origin = point[0] - axis[0]
        y_about_origin = point[1] - axis[1]
        x_new = x_about_origin * c - y_about_origin * s
        y_new = x_about_origin * s + y_about_origin * c
        x_f = x_new + axis[0]
        y_f = y_new + axis[1]
        rotated_poly.append((x_f, y_f))
    return rotated_poly

def draw_angled_poly(pos, color, angle, size):
    x, y = (pos[0], pos[1])
    poly = [(x,y+1),(x+1,y+1),(x+2,y+2),(x+3,y+1),(x+4,y+2),(x+3,y+3),(x+2,y+2),(x+1,y+3),(x,y+3)]
    rotation_axis = (pos[0] + 2, pos[1] + 2)
    poly = rotate_polygon(poly, rotation_axis, angle)
    poly_new = []
    for p in poly:
        poly_new.append((p[0] + size * .5, p[1] + size * .5))
    pygame.draw.polygon(screen, color, poly_new)

# intersection check logic borrowed from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def inRect(p, q, r):
    if q[0] <= max(p[0], r[0]) and q[0] >= min(p[0], r[0]) and q[1] <= max(p[1],r[1]) and q[1] >= min(p[1],r[1]):
        return True
    return False

def orientation(p, q, r):
    # collinear: 0, cw: 1, ccw: 2
    val = (q[1]-p[1]) * (r[0]-q[0]) - (q[0]-p[0]) * (r[1]-q[1])
    if val > 0: return 1
    if val < 0: return 2
    return 0

def check_line_intersection(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and inRect(p1, p2, q1):
        return True
    if o2 == 0 and inRect(p1, q2, q1):
        return True
    if o3 == 0 and inRect(p2, p1, q2):
        return True
    if o4 == 0 and inRect(p2, q1, q2):
        return True
    return False

class wall:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

window_borders = [((0, 0), (WINDOW[0], 10)), ((0, 0), (10, WINDOW[1])), ((0, WINDOW[1] - 10), (WINDOW[0], 10)), ((WINDOW[0] - 10, 0), (10, WINDOW[1]))]
wall_coordinates = [((490, 310), (10, 80)), ((490, 420), (10, 80)), ((690, 310), (10, 80)), ((690, 420), (10, 80)), ((500, 300), (80, 10)), ((610, 300), (80, 10)), ((500, 500), (80, 10)), ((610, 500), (80, 10))]
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
    def look(self):
        center = (self.pos[0] + .5 * self.size, self.pos[1] + .5 * self.size)
        viewpoint = (center[0] + self.size * .5 + 2*math.cos(self.angle), center[1] + self.size * .5 + 2*math.sin(self.angle))
        for i in range(-45, 45, 9):
            endpoint = (viewpoint[0] + 30*math.cos(self.angle + math.pi * (1/180) * i), viewpoint[1] + 30*math.sin(self.angle + math.pi * (1/180) * i))
            pygame.draw.line(surface, (255, 255, 255, 50), viewpoint, endpoint, 1)
    def explore(self):
        self.angle = self.angle + (random.random() * 2 - 1) * delta_time * speed
        #TODO make it so collisions happen from center w/o phasing through walls
        center = self.pos #( self.pos[0] + size * .5, self.pos[1] + size * .5)
        x_movement = math.cos(self.angle) * delta_time * speed
        if (x_movement > 0): center = (center[0] + size, center[1])
        y_movement = math.sin(self.angle) * delta_time * speed
        if (y_movement > 0): center = (center[0], center[1] + size)
        new_x = self.pos[0] + x_movement
        new_y = self.pos[1] + y_movement
        for w in walls:
            p1 = w.pos
            p2 = (w.pos[0] + w.size[0], w.pos[1])
            p3 = (w.pos[0] + w.size[0], w.pos[1] + w.size[1])
            p4 = (w.pos[0], w.pos[1] + w.size[1])
            for p in [(p1,p2), (p2,p3), (p3,p4), (p4,p1)]:
                if check_line_intersection(center, (new_x, center[1]), p[0], p[1]):
                    new_x = self.pos[0]
                if check_line_intersection(center, (center[0], new_y), p[0], p[1]):
                    new_y = self.pos[1]
        self.pos = (new_x, new_y)

ants = []

for i in range (500):
    pos = (600, 400)
    #pos = (random.randint(10, 1190), random.randint(10, 790))
    color = (random.randint(50, 205), random.randint(50, 205), random.randint(50, 205))
    angle = (random.random() * math.pi * 2)
    speed = 20
    size = 4
    ants.append(ant(pos, color, angle, 20, 4))

while run:
    delta_time = time.time() - prev_time
    prev_time = time.time()
    screen.fill((0, 0, 0))
    surface.fill((0,0,0,0))

    for a in ants:
        a.explore()
        a.look()
        draw_angled_poly(a.pos, a.color, a.angle, 4)

    for w in walls:
        pygame.draw.rect(screen, (155,155,155), (w.pos, w.size))

    screen.blit(surface, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

