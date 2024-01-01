import pygame, numpy as np, time
import settings, inputs, surface, gridcell
import ant, wall, pheromone, food
import shared


prev_time = time.time()
delta_time = time.time()
pygame.init()

#Initialize grid
grid_cells = np.zeros((settings.c_cols, settings.c_rows), dtype = gridcell.dtype)
gridcell.initialize(grid_cells)

#Draw gridlines
gridcell.draw_gridlines()

#Draw walls
wall.set(grid_cells)
wall.draw(grid_cells)

#Set food
#grid_cells[10: settings.c_rows-10,25:35]['food'] = 1000

#Initialize ants
ant.initialize(shared.ants)

run = True
while (run):

    # Calculate time between frames
    delta_time = min(settings.max_dt, time.time() - prev_time)
    prev_time = time.time()

    # Clear screen
    surface.screen.fill((0,0,0))

    # Run for a fixed time to time functions when profiling
    if settings.debug_timed_run:
        settings.debug_timed_run_timer -= delta_time
        if settings.debug_timed_run_timer <= 0:
            run = False

    # Event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            inputs.keypress(e.key)

    # Handle ant movement
    ant.update_pos(shared.ants, grid_cells, delta_time)

    # Update pheromone grid and gradient
    pheromone.update_pheromones(grid_cells, shared.ants, delta_time)

    # Update food grid
    food.update_cell_food(grid_cells)

    # Draw ants
    ant.draw(shared.ants, surface.ants)
    
    # Combine all layers and display
    surface.update_screen()

    pygame.display.update()

pygame.quit()