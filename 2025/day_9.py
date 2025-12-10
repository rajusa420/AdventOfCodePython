from itertools import combinations
from utils import polygon_utils

def do_part_1(file_path="2025/input/day_9_input.txt"):
    points = []
    with open(file_path, "r") as file:
        for line in file:
            x, y = map(int, line.strip().split(","))
            points.append((x, y))

    max_area = 0
    for point_1, point_2 in combinations(points, 2):
        x_1, y_1 = point_1
        x_2, y_2 = point_2

        area = abs(x_1 - x_2 + 1) * abs(y_1 - y_2 + 1)
        if area > max_area:
            max_area = area
    
    return max_area

def do_part_2(file_path="2025/input/day_9_input.txt"):
    points = []
    with open(file_path, "r") as file:
        for line in file:
            x, y = map(int, line.strip().split(","))
            points.append((x, y))

    max_area = 0
    # Only check rectangles where both diagonal corners are polygon vertices (red tiles)
    for point_1, point_2 in combinations(points, 2):
        x_1, y_1 = point_1
        x_2, y_2 = point_2

        if x_1 == x_2 or y_1 == y_2:
            continue

        min_x = min(x_1, x_2)
        max_x = max(x_1, x_2)
        min_y = min(y_1, y_2)
        max_y = max(y_1, y_2)
        rect_corners = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]

        if polygon_utils.is_rect_in_polygon(rect_corners, points):
            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            if area >= max_area:
                print(f"New max area {area} with corners {point_1} and {point_2}")
                max_area = area

    return max_area

if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_9_input.txt")
    #print(f"Part 1: Result: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_9_input.txt")
    print(f"Part 2: Result: {part_2_result}") 
    # 1665679194