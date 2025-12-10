def is_point_on_segment(point, seg_start, seg_end):
    """Check if a point lies on a line segment."""
    px, py = point
    x1, y1 = seg_start
    x2, y2 = seg_end

    # Check if point is collinear with segment
    cross = (py - y1) * (x2 - x1) - (px - x1) * (y2 - y1)
    if cross != 0:
        return False

    # Check if point is within segment bounds
    return min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2)

def is_point_on_polygon_boundary(point, polygon_points):
    """Check if a point lies on any edge of the polygon."""
    total_points = len(polygon_points)
    for i in range(total_points):
        if is_point_on_segment(point, polygon_points[i], polygon_points[(i + 1) % total_points]):
            return True
    return False

def is_point_in_polygon(point, polygon_points):
    """Ray casting algorithm - count edge crossings to the right of point."""
    x, y = point
    inside = 0
    n = len(polygon_points)

    for i in range(n):
        x1, y1 = polygon_points[i]
        x2, y2 = polygon_points[(i + 1) % n]

        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside += 1

    return inside % 2 == 1

def do_lines_insersect(point_1, point_2, point_3, point_4):
    """Check if two line segments properly intersect (cross each other).
    Returns False if they only touch at endpoints or T-junctions."""
    # If segments share an endpoint, they don't "properly" intersect
    if point_1 == point_3 or point_1 == point_4 or point_2 == point_3 or point_2 == point_4:
        return False

    # If any endpoint of one segment lies on the other segment, it's a T-junction, not a crossing
    if is_point_on_segment(point_1, point_3, point_4) or is_point_on_segment(point_2, point_3, point_4):
        return False
    if is_point_on_segment(point_3, point_1, point_2) or is_point_on_segment(point_4, point_1, point_2):
        return False

    x1, y1 = point_1
    x2, y2 = point_2
    x3, y3 = point_3
    x4, y4 = point_4

    def ccw(ax, ay, bx, by, cx, cy):
        return (cy - ay) * (bx - ax) > (by - ay) * (cx - ax)

    # Check if p1 and p2 are on opposite sides of line p3-p4
    side1 = ccw(x1, y1, x3, y3, x4, y4) != ccw(x2, y2, x3, y3, x4, y4)

    # Check if p3 and p4 are on opposite sides of line p1-p2
    side2 = ccw(x1, y1, x2, y2, x3, y3) != ccw(x1, y1, x2, y2, x4, y4)

    return side1 and side2

def get_intersection_point(point_1, point_2, point_3, point_4):
    x1, y1 = point_1
    x2, y2 = point_2
    x3, y3 = point_3
    x4, y4 = point_4

    dx1, dy1 = x2 - x1, y2 - y1
    dx2, dy2 = x4 - x3, y4 - y3

    cross = dx1 * dy2 - dy1 * dx2

    if cross == 0:
        return None 

    dx3, dy3 = x3 - x1, y3 - y1
    t = (dx3 * dy2 - dy3 * dx2) / cross

    # Intersection point
    ix = x1 + t * dx1
    iy = y1 + t * dy1

    return (ix, iy)

def is_point_in_or_on_polygon(point, polygon_points):
    """Check if a point is inside the polygon OR on its boundary."""
    return is_point_in_polygon(point, polygon_points) or is_point_on_polygon_boundary(point, polygon_points)

def is_rect_in_polygon(rect_corner_points, polygon_points):
    # First check that all rectangle corners are inside or on the polygon boundary
    for point in rect_corner_points:
        if not is_point_in_or_on_polygon(point, polygon_points):
            return False

    # Then check that no rectangle edges cross polygon edges
    rect_edges = [
        (rect_corner_points[0], rect_corner_points[1]),
        (rect_corner_points[1], rect_corner_points[2]),
        (rect_corner_points[2], rect_corner_points[3]),
        (rect_corner_points[3], rect_corner_points[0])
    ]

    total_points = len(polygon_points)
    for i in range(total_points):
        poly_edge = (polygon_points[i], polygon_points[(i + 1) % total_points])
        for rect_edge in rect_edges:
            if do_lines_insersect(rect_edge[0], rect_edge[1], poly_edge[0], poly_edge[1]):
                return False

    return True
    