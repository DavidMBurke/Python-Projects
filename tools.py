import math, pygame

def rotate_polygon(polygon, axis, angle):
    s = math.sin(angle)
    c = math.cos(angle)
    rotated_poly = []
    for point in polygon:
        x_about_origin = point[0] - axis[0]
        y_about_origin = point[1] - axis[1]
        x_new = x_about_origin * c - y_about_origin * s
        y_new = x_about_origin * s + y_about_origin * c
        x_f = x_new + axis[0]
        y_f = y_new + axis[1]
        rotated_poly.append((x_f, y_f))
    return rotated_poly

def draw_angled_poly(screen, poly, pos, color, angle, size):
    x, y = (pos[0], pos[1])
    poly_offset = []
    for p in poly:
        poly_offset.append((x + p[0], y + p[1]))
    rotation_axis = (pos[0] + 2, pos[1] + 2)
    poly = rotate_polygon(poly_offset, rotation_axis, angle)
    pygame.draw.polygon(screen, color, poly)

    # intersection check logic borrowed from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def inRect(p, q, r):
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):        return True
    return False

def orientation(p, q, r):
    # collinear: 0, cw: 1, ccw: 2
    val = (q[1]-p[1]) * (r[0]-q[0]) - (q[0]-p[0]) * (r[1]-q[1])
    if val > .0001: return 1
    if val < .0001: return 2
    return 0

def check_line_intersection(p1, q1, p2, q2):
    if min(p1[0],q1[0]) > max(p2[0],q2[0]) or max(p1[0],q1[0]) < min(p2[0],q2[0]):
        return False
    if min(p1[1],q1[1]) > max(p2[1],q2[1]) or max(p1[1],q1[1]) < min(p2[1],q2[1]):
        return False
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        return True
    if o1 == 0 and inRect(p1, p2, q1):
        return True
    if o2 == 0 and inRect(p1, q2, q1):
        return True
    if o3 == 0 and inRect(p2, p1, q2):
        return True
    if o4 == 0 and inRect(p2, q1, q2):
        return True
    return False

def sign(n):
    if n > 0 : return 1
    if n < 0 : return -1
    return 0