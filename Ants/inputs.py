import pygame, settings, shared

# Show gridlines - g
# Show pheromones - p
# Show pheromone gradient - v

def keypress(key):
    match key:
        case pygame.K_f:
            shared.ants['food'] = 100
        case pygame.K_g:
            settings.debug_show_grid = ~settings.debug_show_grid
        case pygame.K_p:
            settings.debug_show_pheromones = ~settings.debug_show_pheromones
        case pygame.K_v:
            if (not settings.debug_show_gradient_colors and not settings.debug_show_gradient_arrows):
                settings.debug_show_gradient_colors = True
            elif (settings.debug_show_gradient_colors):
                settings.debug_show_gradient_colors = False
                settings.debug_show_gradient_arrows = True
            else:
                settings.debug_show_gradient_colors = False
                settings.debug_show_gradient_arrows = False