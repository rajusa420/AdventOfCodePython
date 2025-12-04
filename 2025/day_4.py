import grid_utils

def check_adjacent_rolls(grid, row, col, row_count, col_count, max_allowed):
    adjacent_roll_count = 0

    for dx, dy in grid_utils.adjacent_directions_offsets:
        new_row = row + dx
        new_col = col + dy

        if new_row < 0 or new_row >= row_count or new_col < 0 or new_col >= col_count:
            continue

        if grid[new_row][new_col] == '@':
            adjacent_roll_count += 1

        if adjacent_roll_count >= max_allowed:
            return False

    return True

def do_part_1(file_path="day_4_input.txt"):
    toilet_paper_roll_count = 0
    with open(file_path, "r") as file:
        grid = grid_utils.populate_string_grid(file)
        row_count = len(grid)
        col_count = len(grid[0]) if row_count > 0 else 0

        for row in range(row_count):
            for col in range(col_count):
                # First is there a roll on this spot
                if grid[row][col] != '@':
                    continue

                if check_adjacent_rolls(grid, row, col, row_count, col_count, 4):
                    toilet_paper_roll_count += 1

    return toilet_paper_roll_count

def do_part_2(file_path="day_4_input.txt"):
    toilet_paper_roll_count = 0
    with open(file_path, "r") as file:
        grid = grid_utils.populate_string_grid(file)
        row_count = len(grid)
        col_count = len(grid[0]) if row_count > 0 else 0

        while True:
            locations_to_remove= []
            for row in range(row_count):
                for col in range(col_count):
                    # First is there a roll on this spot
                    if grid[row][col] != '@':
                        continue

                    if check_adjacent_rolls(grid, row, col, row_count, col_count, 4):
                        toilet_paper_roll_count += 1
                        locations_to_remove.append((row, col))
            
            if len(locations_to_remove) == 0:
                break

            for location in locations_to_remove:
                grid[location[0]][location[1]] = 'x'

    return toilet_paper_roll_count

if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_4_input.txt")
    #print(f"Part 1: Total toilet roll count: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_4_input.txt")
    print(f"Part 2: Total toilet roll count: {part_2_result}")