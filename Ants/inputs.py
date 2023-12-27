import pygame, settings

def keypress(key):
    match key:
        case pygame.K_g:
            settings.debug_show_grid = not settings.debug_show_grid
        case pygame.K_v:
            settings.debug_show_gradient = not settings.debug_show_gradient
        case pygame.K_p:
            settings.debug_show_pheromones = not settings.debug_show_pheromones