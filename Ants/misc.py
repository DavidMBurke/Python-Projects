import pygame, math

def rotate_polygon(polygon, axis, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    rotated_poly = []
    for point in polygon:
        # Transpose poly to origin
        x_about_origin = point[0] - axis[0]
        y_about_origin = point[1] - axis[1]
        # Displace each point by angle relative to origin
        x_new = x_about_origin * c - y_about_origin * s
        y_new = x_about_origin * s + y_about_origin * c
        # Transpose back to axis position
        x_f = x_new + axis[0]
        y_f = y_new + axis[1]
        # Add point to new poly
        rotated_poly.append((x_f, y_f))
    return rotated_poly


#TODO make modular, currently hardcoded for arrows of a fixed size
def draw_angled_poly(pos, color, angle, size, screen):
    x, y = (pos[0], pos[1])
    arrow = [(x,y+2),(x,y+3),(x+3,y+3),(x+3,y+5),(x+5,y+3),(x+5,y+2),(x+3,y),(x+3,y+2),(x,y+2)]
    rotation_axis = (pos[0] + 2, pos[1] + 2)
    arrow = rotate_polygon(arrow, rotation_axis, angle)
    for p in arrow:
        p = (p[0] + size * .5, p[1] + size * .5)
    pygame.draw.polygon(screen, color, arrow)