def populate_string_grid(file):
    grid = []
    for line in file:
        row = list(line.strip())
        grid.append(row)
    return grid

adjacent_directions_offsets = [(-1, -1), (0, -1), (1, -1), 
                               (-1,  0),          (1,  0),
                               (-1,  1), (0,  1), (1,  1)]
