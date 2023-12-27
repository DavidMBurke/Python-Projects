import pygame, numpy as np, scipy as sp, math
import ant, surface, settings, misc

#Update the 'pheromone' and 'food' values of each cell TODO - move food to its own logic
def update_cells(grid_cells):
    grid_cells['pheromones'] = np.clip(grid_cells['pheromones'] - settings.p_decrease, 0, 255)
    pixels = pygame.surfarray.pixels2d(surface.pheromones)
    pixel_alphas = pygame.surfarray.pixels_alpha(surface.pheromones)
    p = grid_cells['pheromones']
    f = grid_cells['food']
    colors = (p[:,:,0] << 16) + (p[:,:,1] << 8) + (p[:,:,2])
    colors[f > 0] = 16711935
    colors = np.repeat(colors, settings.c_size, axis = 0) #Expand to size of window
    colors = np.repeat(colors, settings.c_size, axis = 1)
    pixels[:] = colors
    pixel_alphas[colors != 0] = 100
    del pixels
    del pixel_alphas

# Kernal size to simulate ant vision from each square on grid, and show area of highest concentration
kernel_side = 2 * settings.ant_sight + 1
kernel_x = np.zeros((kernel_side, kernel_side))
kernel_x[:settings.ant_sight, :] = 1
kernel_x[1+settings.ant_sight:, :] = -1
kernel_y = np.zeros((kernel_side, kernel_side))
kernel_y[:,:settings.ant_sight] = 1
kernel_y[:,1+settings.ant_sight:] = -1

# Find the gradient of pheromones from each square
# TODO Find a way to optimize or put into shaders, currently creates lag spikes
def update_gradient(grid_cells):
    p = grid_cells['pheromones'][:,:,0] # r pheromone
    
    gradient_x = sp.ndimage.convolve(p, kernel_x, mode='constant', cval = 0)
    gradient_y = sp.ndimage.convolve(p, kernel_y, mode='constant', cval = 0)
    # Find the direction in radians to highest concentration
    gradient = np.arctan2(gradient_y,gradient_x)
    
    if settings.debug_show_gradient_colors:
        pixels = pygame.surfarray.pixels2d(surface.gradient)
        pixel_alphas = pygame.surfarray.pixels_alpha(surface.gradient)
        c = np.zeros_like(gradient)
        c[gradient > 0] = (255 * gradient[gradient > 0] * math.pi).astype(int) << 16
        c[gradient < 0] = (255 * gradient[gradient < 0] * -math.pi).astype(int)
        temp = np.repeat(c, settings.c_size, axis=0)
        pixels[:] = np.repeat(temp, settings.c_size, axis=1)
        pixel_alphas.fill(0)
        pixel_alphas[pixels != 0] = 100

        del pixels
        del pixel_alphas

    if settings.debug_show_gradient_arrows:
        surface.gradient.fill((0, 0, 0, 0))
        for index, angle in np.ndenumerate(gradient):
            if (index[0] % 3 == 0 and index[1] % 3 == 0):
                pos = (index[0] * settings.c_size, index[1] * settings.c_size)
                misc.draw_angled_poly(pos, (255,255,255), angle, 10, surface.gradient)


def update_pheromones(grid_cells, ants, delta_time):
    settings.pheromone_timer -= delta_time
    while settings.pheromone_timer <= 0:
        settings.pheromone_timer += settings.p_update_speed
        ant.drop_pheromones(ants, grid_cells)
        update_cells(grid_cells)
    settings.gradient_timer -= delta_time
    while settings.gradient_timer <= 0:
        update_gradient(grid_cells)
        settings.gradient_timer += settings.gradient_update_speed