import pygame
import math

def draw_gradient_circle(screen, x, y, radius, color):
    """
    Draws a circle with a gradient from solid to transparent on the screen.
    :param screen: Pygame screen surface to draw on.
    :param x: X-coordinate of the circle's center.
    :param y: Y-coordinate of the circle's center.
    :param radius: Radius of the circle.
    :param color: Base color of the circle.
    """
    # Create a new surface with an alpha channel for transparency
    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

    # Draw the gradient circle
    for dy in range(-radius, radius):
        for dx in range(-radius, radius):
            distance = math.sqrt(dx**2 + dy**2)

            if distance < radius:
                alpha = 255 - int((distance / radius) * 255)
                gradient_color = (*color[:3], alpha)  # Use the base color with varying alpha
                circle_surface.set_at((dx + radius, dy + radius), gradient_color)

    # Blit the circle surface onto the main screen
    screen.blit(circle_surface, (x - radius, y - radius))

# Pygame initialization
pygame.init()

# Screen dimensions and setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Fill screen with black
    draw_gradient_circle(screen, 400, 300, 100, (255, 0, 0))  # Example usage
    pygame.display.flip()

pygame.quit()