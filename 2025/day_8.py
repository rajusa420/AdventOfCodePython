from itertools import combinations

def euclid_distance(point1, point2):
    point1_x, point1_y, point1_z = point1
    point2_x, point2_y, point2_z = point2
    return ((point1_x - point2_x) ** 2) + ((point1_y - point2_y) ** 2) + ((point1_z - point2_z) ** 2)

def do_part_1(file_path="day_8_input.txt", distance_threshold=10):
    nodes = []
    with open(file_path, "r") as file:
        for line in file:
            points = map(int, line.split(","))
            nodes.append(tuple(points))
    node_count = len(nodes)

    distance_map = {}
    for node_1, node_2 in combinations(nodes, 2):
        distance = euclid_distance(node_1, node_2)
        distance_map[distance] = (node_1, node_2)

    distances = sorted(distance_map.keys())

    # map from node to circuit index
    visited_nodes = {}
    circuits = []

    for distance_index in range(distance_threshold):
        distance = distances[distance_index]
        node_1, node_2 = distance_map[distance]
        
        if node_1 in visited_nodes and node_2 in visited_nodes:
            circuit_index_1 = visited_nodes[node_1]
            circuit_index_2 = visited_nodes[node_2]
            if circuit_index_1 != circuit_index_2:
                # Merge circuits
                circuit_2_nodes = circuits[circuit_index_2]
                circuits[circuit_index_1] += circuit_2_nodes

                # Now mark all the circuit 2 nodes as part of circuit 1
                for node in circuit_2_nodes:
                    visited_nodes[node] = circuit_index_1

                # Remove the merged circuit
                circuits[circuit_index_2] = []

        elif node_1 in visited_nodes:
            circuit_index = visited_nodes[node_1]
            circuits[circuit_index].append(node_2)
            visited_nodes[node_2] = circuit_index
        elif node_2 in visited_nodes:
            circuit_index = visited_nodes[node_2]
            circuits[circuit_index].append(node_1)
            visited_nodes[node_1] = circuit_index
        else:
            # New circuit
            circuits.append([node_1, node_2])
            circuit_index = len(circuits) - 1
            visited_nodes[node_1] = circuit_index
            visited_nodes[node_2] = circuit_index
    
    circuits.sort(key=lambda x: len(x), reverse=True)

    product = 1
    for circuit_index in range(3):
        circuit_size = len(circuits[circuit_index])
        product *= circuit_size
        # print(f"Circuit {circuit_index}: Node Count: {len(circuits[circuit_index])}")
    return product

def do_part_2(file_path="day_8_input.txt"):
    nodes = []
    with open(file_path, "r") as file:
        for line in file:
            points = map(int, line.split(","))
            nodes.append(tuple(points))
    node_count = len(nodes)

    distance_map = {}
    for node_1, node_2 in combinations(nodes, 2):
        distance = euclid_distance(node_1, node_2)
        distance_map[distance] = (node_1, node_2)

    distances = sorted(distance_map.keys())

    # map from node to circuit index
    visited_nodes = {}
    circuits = []

    for distance in distances:
        node_1, node_2 = distance_map[distance]
        
        new_circuit_len = 0
        if node_1 in visited_nodes and node_2 in visited_nodes:
            circuit_index_1 = visited_nodes[node_1]
            circuit_index_2 = visited_nodes[node_2]
            if circuit_index_1 != circuit_index_2:
                # Merge circuits
                circuit_2_nodes = circuits[circuit_index_2]
                circuits[circuit_index_1] += circuit_2_nodes

                # Now mark all the circuit 2 nodes as part of circuit 1
                for node in circuit_2_nodes:
                    visited_nodes[node] = circuit_index_1

                # Remove the merged circuit
                circuits[circuit_index_2] = []
                new_circuit_len = len(circuits[circuit_index_1])

        elif node_1 in visited_nodes:
            circuit_index = visited_nodes[node_1]
            circuits[circuit_index].append(node_2)
            visited_nodes[node_2] = circuit_index
            new_circuit_len = len(circuits[circuit_index])
        elif node_2 in visited_nodes:
            circuit_index = visited_nodes[node_2]
            circuits[circuit_index].append(node_1)
            visited_nodes[node_1] = circuit_index
            new_circuit_len = len(circuits[circuit_index])
        else:
            # New circuit
            circuits.append([node_1, node_2])
            circuit_index = len(circuits) - 1
            visited_nodes[node_1] = circuit_index
            visited_nodes[node_2] = circuit_index
        
        if new_circuit_len >= node_count:
            x1, y1, z1 = node_1
            x2, y2, z2 = node_2
            return x1 * x2
    
    return 0



if __name__ == "__main__":
    # part_1_result = do_part_1("2025/input/day_8_test.txt")
    # part_1_result = do_part_1("2025/input/day_8_input.txt", distance_threshold=1000)
    # print(f"Part 1: Result: {part_1_result}")
    part_2_result = do_part_2("2025/input/day_8_input.txt")
    print(f"Part 2: Result: {part_2_result}")