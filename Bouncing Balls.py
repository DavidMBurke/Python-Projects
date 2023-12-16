import pygame, time, random, math, numpy

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
gravity = .2
prev_time = time.time()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Particle:
  def __init__(self, pos, r, density, color, damping, vel = (0,0)):
    self.pos = pos
    self.r = r
    self.density = density
    self.volume = math.pi * pow(r, 2)
    self.mass = self.volume / self.density
    self.color = color
    self.damping = damping
    self.vel = vel
  def resolve_collisions(self):
    #Boundary Collisions
    if p.pos[0] < p.r:
      p.pos[0] = 2 * p.r - p.pos[0]
      p.vel[0] = -p.vel[0] * p.damping
    if p.pos[0] > SCREEN_WIDTH - p.r:
      p.pos[0] = SCREEN_WIDTH - (p.pos[0] - SCREEN_WIDTH) - 2 * p.r
      p.vel[0] = -p.vel[0] * p.damping
      if abs(p.vel[0]) < .1:
        p.vel[0] = 0
    if p.pos[1] < p.r:
      p.pos[1] = 2 * p.r -p.pos[1]
      p.vel[1] = -p.vel[1] * p.damping
    if p.pos[1] > SCREEN_HEIGHT - p.r:
      p.pos[1] = SCREEN_HEIGHT - (p.pos[1] - SCREEN_HEIGHT) - 2 * p.r
      p.vel[1] = -p.vel[1] * p.damping
      if abs(p.vel[1]) < .1:
        p.vel[1] = 0
    #Collisions with other particles
    for p2 in particles:
      if p2 is p:
        continue
      dist = math.sqrt( pow(p.pos[0] - p2.pos[0], 2) + pow(p.pos[1] - p2.pos[1], 2))
      #relV = math.sqrt( pow(p.vel[0] - p2.vel[0], 2) + pow(p.vel[1] - p2.vel[1], 2))
      if dist < p.r + p2.r: # and relV > p.damping:
        p.vel = p.vel - (2 * p2.mass / (p.mass + p2.mass)) * (numpy.dot(p.vel - p2.vel, p.pos - p2.pos) / pow(dist, 2)) * (p.pos-p2.pos)
        p2.vel = p2.vel - (2 * p.mass / (p2.mass + p.mass)) * (numpy.dot(p2.vel - p.vel, p2.pos - p.pos) / pow(dist, 2)) * (p2.pos-p.pos)
        direction = (p2.pos - p.pos)
        overlap = p.r + p2.r - dist
        p.pos[0] -= direction[0] * overlap * (p.r / (p.r + p2.r))
        p.pos[1] -= direction[1] * overlap * (p.r / (p.r + p2.r))
        p2.pos[0] += direction[0] * overlap * (p2.r / (p.r + p2.r))
        p2.pos[1] += direction[1] * overlap * (p2.r / (p.r + p2.r))

particles = []
for i in range(20):
  x = random.randint(0, SCREEN_WIDTH)
  y = random.randint(0, SCREEN_HEIGHT)
  r = random.randint(2, 10)
  color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
  damping = .8
  velocity = (random.randint(-200,200), 0)
  particles.append(Particle((x, y), r, 1, color, damping, velocity))

run = True
while run:
  delta_time = time.time() - prev_time
  prev_time = time.time()
  screen.fill((0,0,0))
  
  for p in particles:
    p.vel += pygame.Vector2(0, 1) * gravity
    p.pos += p.vel * delta_time
    p.resolve_collisions()
    pygame.draw.circle(screen, p.color, p.pos, p.r)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  pygame.display.update()

pygame.quit()