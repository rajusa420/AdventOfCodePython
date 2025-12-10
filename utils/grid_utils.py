def populate_character_grid(file):
    grid = []
    for line in file:
        row = list(line.strip())
        grid.append(row)
    return grid

def populate_string_grid(file):
    grid = []
    for line in file:
        row = line.split(' ')
        stripped = [str.strip() for str in row if str.strip()]
        grid.append(stripped)
    return grid

def get_column_from_grid(grid, col_index):
    column = [row[col_index] for row in grid]
    return column

adjacent_directions_offsets = [(-1, -1), (0, -1), (1, -1), 
                               (-1,  0),          (1,  0),
                               (-1,  1), (0,  1), (1,  1)]
