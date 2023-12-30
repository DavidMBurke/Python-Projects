import pygame, numpy as np, scipy as sp, math
import ant, surface, settings, misc

#Update the 'pheromone' and 'food' values of each cell TODO - move food to its own logic
def update_cells(grid_cells):
    # Reduce all pheromones
    grid_cells['pheromones'] = np.clip(grid_cells['pheromones'] - settings.p_decrease, 0, 255)
    # Access pixel canvas
    pixels = pygame.surfarray.pixels2d(surface.pheromones)
    pixel_alphas = pygame.surfarray.pixels_alpha(surface.pheromones)
    p = grid_cells['pheromones']
    f = grid_cells['food']
    # Calculate fixed int value for pheromone color
    colors = (p[:,:,0] << 16) + (p[:,:,1] << 8) + (p[:,:,2])
    colors[f > 0] = 16711935
    # Expand array to canvas size
    colors = np.repeat(colors, settings.c_size, axis = 0)
    colors = np.repeat(colors, settings.c_size, axis = 1)
    # Assign colors
    pixels[:] = colors
    pixel_alphas[colors != 0] = 100
    # Delete canvas variables to unlock canvas
    del pixels
    del pixel_alphas

# Kernel sized to simulate ant vision from each square on grid, and show area of highest concentration
#  x kernel:         y kernel: 
#  1, 1, 0,-1,-1     1, 1, 1, 1, 1
#  1, 1, 0,-1,-1     1, 1, 1, 1, 1
#  1, 1, 0,-1,-1     0, 0, 0, 0, 0
#  1, 1, 0,-1,-1    -1,-1,-1,-1,-1
#  1, 1, 0,-1,-1    -1,-1,-1,-1,-1

kernel_side = 2 * settings.ant_sight + 1
kernel_x = np.zeros((kernel_side, kernel_side))
kernel_x[:settings.ant_sight, :] = 1
kernel_x[1+settings.ant_sight:, :] = -1
kernel_y = np.zeros((kernel_side, kernel_side))
kernel_y[:,:settings.ant_sight] = 1
kernel_y[:,1+settings.ant_sight:] = -1

# Find the gradient of pheromones from each square
# TODO Find a way to optimize or put into shaders, currently creates lag spikes at high resolutions
def update_gradient(grid_cells):
    p1 = grid_cells['pheromones'][:,:,0] # red (explore) pheromone
    
    p1_gradient_x = sp.ndimage.convolve(p1, kernel_x, mode='constant', cval = 0)
    p1_gradient_y = sp.ndimage.convolve(p1, kernel_y, mode='constant', cval = 0)
    # Find the direction in radians to highest concentration in view
    p1_gradient = np.arctan2(p1_gradient_y,p1_gradient_x)
    grid_cells[:,:]['p1_gradient'] = p1_gradient
    
    # view of positive / negative gradient (ranging from -pi to pi)
    # Not particularly useful  visual after adding gradient arrow view but kept in case I want to expand on it later
    if settings.debug_show_gradient_colors:
        # Access pixel canvas
        pixels = pygame.surfarray.pixels2d(surface.gradient)
        pixel_alphas = pygame.surfarray.pixels_alpha(surface.gradient)
        c = np.zeros_like(p1_gradient)
        # Apply red where gradient is 0 to pi and blue where -pi to pi
        c[p1_gradient > 0] = (255 * p1_gradient[p1_gradient > 0] * math.pi).astype(int) << 16
        c[p1_gradient < 0] = (255 * p1_gradient[p1_gradient < 0] * -math.pi).astype(int)
        # Expand by multiplier of cell size to equal size of canvas
        temp = np.repeat(c, settings.c_size, axis=0)
        pixels[:] = np.repeat(temp, settings.c_size, axis=1)
        # Set canvas transparent where gradient = 0, and translucent elsewhere 
        pixel_alphas.fill(0)
        pixel_alphas[pixels != 0] = 100
        # Unlock canvas
        del pixels
        del pixel_alphas

    # View of arrows pointing in the direction of pheromones
    if settings.debug_show_gradient_arrows:
        # Reset surface
        surface.gradient.fill((0, 0, 0, 0))
        for index, angle in np.ndenumerate(p1_gradient):
            if (index[0] % 3 == 0 and index[1] % 3 == 0):
                # Draw arrow on cell pointed toward direction of gradient
                pos = (index[0] * settings.c_size, index[1] * settings.c_size)
                misc.draw_angled_poly(pos, (255,255,255), angle, 10, surface.gradient)


def update_pheromones(grid_cells, ants, delta_time):
    #decrease pheromone_timer and if enough time has elapsed, drop pheromones from each ant and update grid and reset timer
    settings.pheromone_timer -= delta_time
    while settings.pheromone_timer <= 0:
        settings.pheromone_timer += settings.p_update_speed
        ant.drop_pheromones(ants, grid_cells)
        update_cells(grid_cells)

    #decrease gradient timer and if enough time has elapsed, update gradient map and reset timer
    settings.gradient_timer -= delta_time
    while settings.gradient_timer <= 0:
        update_gradient(grid_cells)
        settings.gradient_timer += settings.gradient_update_speed