import pygame

run = True
window_dimensions = (800, 600)
screen = pygame.display.set_mode(window_dimensions)


while (run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False