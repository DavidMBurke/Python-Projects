import pygame, settings, shared

# Set food 0 - '-'
# Set food 100 - '='
# Show food - f
# Show gridlines - g
# Show pheromones - p
# Show pheromone gradient - v

def keypress(key):
    match key:
        case pygame.K_EQUALS:
            shared.ants['food'] = 100
        case pygame.K_MINUS:
            shared.ants['food'] = 0
        case pygame.K_f:
            settings.debug_show_food = not settings.debug_show_food
        case pygame.K_g:
            settings.debug_show_grid = not settings.debug_show_grid
        case pygame.K_p:
            settings.debug_show_pheromones = not settings.debug_show_pheromones
        case pygame.K_v:
            # Cycle through color gradient and arrow gradient views
            if (not settings.debug_show_gradient_colors and not settings.debug_show_gradient_arrows):
                settings.debug_show_gradient_colors = True
            elif (settings.debug_show_gradient_colors):
                settings.debug_show_gradient_colors = False
                settings.debug_show_gradient_arrows = True
            else:
                settings.debug_show_gradient_colors = False
                settings.debug_show_gradient_arrows = False