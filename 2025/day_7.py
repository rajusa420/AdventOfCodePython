import grid_utils
from functools import cache

def do_part_1(file_path="day_7_input.txt"):
    splits = 0
    grid = []
    with open(file_path, "r") as file:
        grid = grid_utils.populate_character_grid(file)

    row_count = len(grid)
    col_count = len(grid[0]) if row_count > 0 else 0

    light_grid = [['.' for _ in range(col_count)] for _ in range(row_count)]

    for row_index in range(row_count-1):
        row = grid[row_index]

        for col_index in range(col_count):
            char = row[col_index]

            if char == 'S':
                # First row just populate where the light will be on the second row
                light_grid[row_index + 1][col_index] = '|'
            elif char == '.':
                # Go straight through
                if light_grid[row_index][col_index] == '|':
                    light_grid[row_index + 1][col_index] = '|'
            elif char == '^':
                # Split the light
                if light_grid[row_index][col_index] == '|':
                    splits += 1
                    if col_index > 0:
                        light_grid[row_index + 1][col_index - 1] = '|'

                    if col_index < col_count - 1:
                        light_grid[row_index + 1][col_index + 1] = '|'

    return splits

def do_part_2(file_path="day_7_input.txt"):
    timelines = 0
    grid = []
    with open(file_path, "r") as file:
        grid = grid_utils.populate_character_grid(file)

    row_count = len(grid)
    col_count = len(grid[0]) if row_count > 0 else 0

    @cache
    def process_row(row_index, col_index):
        if row_index >= row_count - 1:
            return 1
        
        char = grid[row_index][col_index]
        if char == '.':
            return process_row(row_index + 1, col_index)
        elif char == '^':
            timelines = 0
            # Split the light
            if col_index > 0:
                timelines += process_row(row_index + 1, col_index - 1)

            if col_index < col_count - 1:
                timelines += process_row(row_index + 1, col_index + 1)

            return timelines
    
    first_row = grid[0]
    for col_index in range(col_count):
        char = first_row[col_index]
        if char == 'S':
            timelines += process_row(1, col_index)

    return timelines

if __name__ == "__main__":
    part_1_splits = do_part_1("2025/input/day_7_input.txt")
    print(f"Part 1: Number of splits: {part_1_splits}")

    part_2_timelines = do_part_2("2025/input/day_7_input.txt")
    print(f"Part 2: Number of timelines: {part_2_timelines}")