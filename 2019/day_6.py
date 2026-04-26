from functools import cache

class SpaceObject:
    def __init__(self, name):
        self.name = name
        self.parent_objects = []
        self.child_objects = []
    
    def add_parent(self, parent):
        self.parent_objects.append(parent)

    def add_child(self, child):
        self.child_objects.append(child)

space_object_map = {}
def get_space_object(name):
    if name not in space_object_map:
        space_object_map[name] = SpaceObject(name)
    return space_object_map[name]

@cache
def get_total_orbitals(space_object, depth):
    total = 0
    for child_space_object in space_object.child_objects:
        total += get_total_orbitals(child_space_object, depth + 1)

    return total + depth

def populate_space_objects(file_path):
    with open(file_path, "r") as file:
        for line in file:
            parent, child = line.strip().split(')')
            parent_space_object = get_space_object(parent)
            child_space_object = get_space_object(child)

            parent_space_object.add_child(child_space_object)
            child_space_object.add_parent(parent_space_object)

def do_part_1(file_path):
    populate_space_objects(file_path=file_path)
    com_space_object = space_object_map['COM']
    return get_total_orbitals(com_space_object, 0)

class ShortestPathFinder:
    def __init__(self):
        self.shortest_distance_found = 1000000
        self.visited_map = {}

    @cache
    def find_shortest_path(self, space_object, distance):
        if distance > self.shortest_distance_found:
            return
        
        previous_visit_distance = self.visited_map.get(space_object.name, 1000000)
        if distance > previous_visit_distance:
            return
        
        #print(f"Visiting: {space_object.name} - {distance}")
        self.visited_map[space_object.name] = distance

        for next_object in (space_object.parent_objects + space_object.child_objects):
            if next_object.name == "SAN":
                if distance < self.shortest_distance_found:
                    print(f"Reached with distance: {distance}")
                    self.shortest_distance_found = distance
            else:
                self.find_shortest_path(next_object, distance + 1)

def do_part_2(file_path):
    populate_space_objects(file_path=file_path)
    you_space_object = space_object_map['YOU']
    #print(f"{you_space_object.name} - {len(you_space_object.parent_objects)} - {len(you_space_object.child_objects)}")
    path_finder = ShortestPathFinder()
    path_finder.find_shortest_path(you_space_object, -1)
    return path_finder.shortest_distance_found

if __name__ == "__main__":
    result = do_part_2("2019/input/day_6_input.txt")
    print(result)