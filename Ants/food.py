import pygame, numpy as np
import colors, settings, surface

def update_cell_food(grid_cells):
    if settings.debug_show_food:
    # Access pixel canvas
        pixels = pygame.surfarray.pixels2d(surface.food)
        pixel_alphas = pygame.surfarray.pixels_alpha(surface.food)
        f = grid_cells['food']
        # Set food color
        display_colors = np.zeros_like(f)
        display_colors[f > 0] = colors.magenta
        # Expand array to canvas size
        display_colors = np.repeat(display_colors, settings.c_size, axis = 0)
        display_colors = np.repeat(display_colors, settings.c_size, axis = 1)
        # Assign colors
        pixels[:] = display_colors
        pixel_alphas[display_colors != 0] = 100
        # Delete canvas variables to unlock canvas
        del pixels
        del pixel_alphas
