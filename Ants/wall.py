import settings, pygame, surface, numpy as np

def set(grid_cells):
    # Add borders
    grid_cells[:, 0:2]['wall'] = True
    grid_cells[:, settings.c_rows-2:settings.c_rows]['wall'] = True
    grid_cells[0:2, :]['wall'] = True
    grid_cells[settings.c_cols - 2:settings.c_cols, :]['wall'] = True
    if (settings.slotted_box):
        # Draw a square box with slots in the middle
        offset = 50 / settings.c_size
        gap = 10 / settings.c_size
        half = (settings.c_rows * .5, settings.c_cols * .5)
        grid_cells[int(half[0] - offset) : int(half[0] - gap), int(half[1] - offset)]['wall'] = True
        grid_cells[int(half[0] + gap) : int(half[0] + offset), int(half[1] - offset)]['wall'] = True
        grid_cells[int(half[0] - offset) : int(half[0] - gap), int(half[1] + offset)]['wall'] = True
        grid_cells[int(half[0] + gap) : int(half[0] + offset), int(half[1] + offset)]['wall'] = True
        grid_cells[int(half[0] - offset), int(half[1] - offset) : int(half[1] - gap)]['wall'] = True
        grid_cells[int(half[0] + offset), int(half[1] - offset) : int(half[1] - gap)]['wall'] = True
        grid_cells[int(half[0] - offset), int(half[1] + gap) : int(half[1] + offset)]['wall'] = True
        grid_cells[int(half[0] + offset), int(half[1] + gap) : int(half[1] + offset)]['wall'] = True

def draw(grid_cells):

    #TODO Use canvas drawing to speed this up
    for (x,y), cell in np.ndenumerate(grid_cells):
        if cell['wall']:
            pygame.draw.rect(surface.wall, (100, 100, 100), (x * settings.c_size, y * settings.c_size, settings.c_size, settings.c_size))
