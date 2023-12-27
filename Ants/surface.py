import settings, pygame

# Main display surface
screen = pygame.display.set_mode(settings.window)
# Display grid cells - g key toggles
grid = pygame.Surface((settings.window), pygame.SRCALPHA)
# Wall surface
wall = pygame.Surface((settings.window), pygame.SRCALPHA)
# Pheromones - p key toggles
pheromones = pygame.Surface((settings.window), pygame.SRCALPHA)
# Gradient of pheromones - v key toggles
gradient = pygame.Surface((settings.window), pygame.SRCALPHA)
# Ant surface
ants = pygame.Surface((settings.window), pygame.SRCALPHA)
# Food surface
food = pygame.Surface((settings.window), pygame.SRCALPHA)

def update_screen():
    if settings.debug_show_grid:
        screen.blit(grid, (0,0))
    if settings.debug_show_gradient_colors:
        screen.blit(gradient, (0,0))
    if settings.debug_show_pheromones:
        screen.blit(pheromones, (0,0))
    screen.blit(wall, (0,0))
    screen.blit(ants, (0,0))
    if settings.debug_show_gradient_colors or settings.debug_show_gradient_arrows:
        screen.blit(gradient, (0,0))