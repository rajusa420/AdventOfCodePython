from functools import cache

def populate_nodes_map(file_path):
    nodes_map = {}
    with open(file_path, "r") as file:
        for line in file:
            line_parts = line.strip().split(" ")
            for part in line_parts:
                if part.endswith(":"):
                    node_id = part[:-1]
                    nodes_map[node_id] = []
                else:
                    nodes_map[node_id].append(part)
    
    return nodes_map

def do_part_1(file_path="day_11_input.txt", start_node="you"):
    nodes_map = populate_nodes_map(file_path)
    
    @cache
    def walk_nodes(current_node):
        connections = nodes_map.get(current_node, [])
        total_paths = 0
        for conn in connections:
            if conn == "out":
                total_paths += 1
            else:
                total_paths += walk_nodes(conn)
        
        return total_paths

    return walk_nodes(start_node)

def do_part_2(file_path="day_11_input.txt"):
    nodes_map = populate_nodes_map(file_path)

    start_node = "svr"
    @cache
    def walk_nodes(current_node, visited):
        connections = nodes_map.get(current_node, [])
        total_paths = 0
        for conn in connections:
            if conn == "out":
                if "dac" in visited and "fft" in visited:
                    total_paths += 1
            else:
                if current_node == "dac" or current_node == "fft":
                    new_visited = visited | {current_node}  # frozenset union
                    total_paths += walk_nodes(conn, new_visited)
                else:
                    total_paths += walk_nodes(conn, visited)

        return total_paths

    return walk_nodes(start_node, frozenset())
if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_11_input.txt", start_node="svr")
    #print(f"Part 1: Result: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_11_input.txt")
    print(f"Part 2: Result: {part_2_result}")