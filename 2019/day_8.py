


def do_part_1(file_path, grid_width, grid_height):
    image_string = ""
    with open(file_path, "r") as file:
        for line in file:
            image_string += line.strip()

    layers = []
    current_grid = [[0] * grid_width for _ in range(grid_height)]
    current_grid_x = 0
    current_grid_y = 0
    current_grid_zero_count = 0
    min_zero_count = grid_width * grid_height
    layer_index_with_fewest_zeros = -1

    for pixel_string in image_string:
        pixel = int(pixel_string)
        current_grid[current_grid_y][current_grid_x] = pixel

        if pixel == 0:
            current_grid_zero_count += 1

        current_grid_x += 1

        if current_grid_x >= grid_width:
            current_grid_x = 0
            current_grid_y += 1

        if current_grid_y >= grid_height:
            current_grid_y = 0
            layers.append(current_grid)
            current_grid = [[0] * grid_width for _ in range(grid_height)]

            if current_grid_zero_count < min_zero_count:
                min_zero_count = current_grid_zero_count
                layer_index_with_fewest_zeros = len(layers) - 1
            current_grid_zero_count = 0
        
    layer_to_process = layers[layer_index_with_fewest_zeros]
    one_count = 0
    two_count = 0
    for row in range(grid_height):
        for col in range(grid_width):
            pixel = layer_to_process[row][col]
            if pixel == 1:
                one_count += 1
            elif pixel == 2:
                two_count += 1

    return one_count * two_count

def do_part_2(file_path, grid_width, grid_height):
    image_string = ""
    with open(file_path, "r") as file:
        for line in file:
            image_string += line.strip()

    layers = []
    current_grid = [[0] * grid_width for _ in range(grid_height)]
    current_grid_x = 0
    current_grid_y = 0

    for pixel_string in image_string:
        pixel = int(pixel_string)
        current_grid[current_grid_y][current_grid_x] = pixel

        current_grid_x += 1

        if current_grid_x >= grid_width:
            current_grid_x = 0
            current_grid_y += 1

        if current_grid_y >= grid_height:
            current_grid_y = 0
            layers.append(current_grid)
            current_grid = [[0] * grid_width for _ in range(grid_height)]
    
    output_grid = [[2] * grid_width for _ in range(grid_height)]
    for layer in layers:
        for row in range(grid_height):
            for col in range(grid_width):
                current_pixel = output_grid[row][col]
                if current_pixel == 2:
                    output_grid[row][col] = layer[row][col]
    
    for row in output_grid:
        print(f"{row}")

if __name__ == "__main__":
    #part_1_result = do_part_1(file_path="2019/input/day_8_input.txt", grid_width=25, grid_height=6)
    #part_1_result = do_part_1(file_path="2019/input/day_8_test.txt", grid_width=3, grid_height=2)

    #part_2_result = do_part_2(file_path="2019/input/day_8_test_2.txt", grid_width=2, grid_height=2)
    part_2_result = do_part_2(file_path="2019/input/day_8_input.txt", grid_width=25, grid_height=6)
    print(f"Part 2 result: {part_2_result}")