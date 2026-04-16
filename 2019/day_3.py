def on_segment(a, b, p):
    return (
        min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) and
        min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
    )

def segment_intersection(p1, p2, q1, q2):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = q1
    x4, y4 = q2

    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denom == 0:
        return None  # parallel or collinear

    px = (
        (x1 * y2 - y1 * x2) * (x3 - x4)
        - (x1 - x2) * (x3 * y4 - y3 * x4)
    ) / denom
    py = (
        (x1 * y2 - y1 * x2) * (y3 - y4)
        - (y1 - y2) * (x3 * y4 - y3 * x4)
    ) / denom

    pt = (px, py)

    if on_segment(p1, p2, pt) and on_segment(q1, q2, pt):
        return pt

    return None

def find_intersection_points(wire_1_points, wire_2_points):
    intersections = []
    for i in range(len(wire_1_points) - 1):
        wire_1_pt1 = wire_1_points[i]
        wire_1_pt2 = wire_1_points[i + 1]

        for j in range(len(wire_2_points) - 1):
            wire_2_pt1 = wire_2_points[j]
            wire_2_pt2 = wire_2_points[j + 1]

            intersection = segment_intersection(
                wire_1_pt1,
                wire_1_pt2,
                wire_2_pt1,
                wire_2_pt2
            )

            if intersection is not None:
                intersections.append(intersection)
    
    return intersections

def get_points(instruction_line):
    wire_points = []
    current_point = (0, 0)
    wire_points.append(current_point)

    for instruction in instruction_line.split(","):
        direction = instruction[0]
        distance = int(instruction[1:])
        x, y = current_point
        match direction:
            case 'U':
                y -= distance
            case 'D':
                y += distance
            case 'R':
                x -= distance
            case 'L':
                x += distance
        
        current_point = (x, y)
        wire_points.append(current_point)
    return wire_points

def get_manhattan_distance(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)

def find_walking_distance(wire_points, end_point):
    walking_distance = 0
    previous_point = None
    for point in wire_points:
        if previous_point is not None:
            if on_segment(previous_point, point, end_point):
                walking_distance += get_manhattan_distance(previous_point, end_point)
                return walking_distance
            walking_distance += get_manhattan_distance(previous_point, point)

        previous_point = point
    return 0

def do_part_2(file_path="2019/input/day_3_input.txt"):
    instruction_line1 = ""
    instruction_line2 = ""
    with open(file_path, "r") as file:
        instruction_line1 = file.readline().strip()
        instruction_line2 = file.readline().strip()

    wire1_points = get_points(instruction_line1)
    wire2_points = get_points(instruction_line2)
    intersection_points = find_intersection_points(wire1_points, wire2_points)

    shortest_walk = 10000000
    for intersection_point in intersection_points:
        if intersection_point == (0, 0):
            continue

        walk_distance_1 = find_walking_distance(wire1_points, intersection_point)

        if walk_distance_1 >= shortest_walk:
            continue

        walk_distance_2 = find_walking_distance(wire2_points, intersection_point)

        if walk_distance_1 == 0 or walk_distance_2 == 0:
            print(f"Fail")

        walk_distance = walk_distance_1 + walk_distance_2
        if walk_distance < shortest_walk:
            shortest_walk = walk_distance
    
    return shortest_walk

def do_part_1(file_path="2019/input/day_3_input.txt"):
    
    instruction_line1 = ""
    instruction_line2 = ""
    with open(file_path, "r") as file:
        instruction_line1 = file.readline().strip()
        instruction_line2 = file.readline().strip()

    wire1_points = get_points(instruction_line1)
    wire2_points = get_points(instruction_line2)

    #print(f"Points={wire1_points}")
    #print(f"Points={wire2_points}")

    intersection_points = find_intersection_points(wire1_points, wire2_points)
    #print(f"Intersection Points={intersection_points}")
    
    shortest_distance = 10000000
    for point in intersection_points:
        distance = get_manhattan_distance(point, (0, 0))
        if distance > 0 and distance < shortest_distance:
            shortest_distance = distance

    return shortest_distance

if __name__ == "__main__":
    result = do_part_2("2019/input/day_3_input.txt")
    print(result)