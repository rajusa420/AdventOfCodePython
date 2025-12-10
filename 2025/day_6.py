
from functools import reduce
from utils import grid_utils

def do_part_1(file_path="day_6_input.txt"):
    sum = 0
    with open(file_path, "r") as file:
        grid = grid_utils.populate_string_grid(file)
        row_count = len(grid)
        col_count = len(grid[0]) if row_count > 0 else 0

        for col in range(col_count):
            column = grid_utils.get_column_from_grid(grid, col)
            operator = column.pop(row_count - 1)
            
            sum += reduce(lambda x, y: x + y if operator == '+' else x * y, map(int, column))
        
    return sum

def do_part_2(file_path="day_6_input.txt"):
    sum = 0
    lines = []
    with open(file_path, "r") as file:
        for line in file:
            lines.append(line)

    # Get operator line to figure out alignment
    operator_line = lines.pop(len(lines) - 1)
    operator_indexes = []
    operators = []
    for index in range(len(operator_line)):
        if operator_line[index] in ['+', '*']:
            operator_indexes.append(index)
            operators.append(operator_line[index])

    # Populate grid based on operator indexes. Fill in the spaces with 'x'
    grid = []
    for line in lines:
        grid_row = []
        previous_index = operator_indexes[0]
        for i in range(1, len(operator_indexes)):
            index = operator_indexes[i]
            current_value_str = line[previous_index:index-1]
            grid_row.append(current_value_str.replace(' ', 'x'))
            
            previous_index = index
        
        # Last value
        current_value_str = line[previous_index:]
        grid_row.append(current_value_str.strip('\n').replace(' ', 'x'))
        grid.append(grid_row)

    row_count = len(grid)
    col_count = len(grid[0]) if row_count > 0 else 0

    # Go through each column in the grid
    for grid_col_index in range(col_count):
        column = grid_utils.get_column_from_grid(grid, grid_col_index)
        operator = operators[grid_col_index]
        #print(f"Column {grid_col_index}: {column} - Operator: {operator}")
        
        operand_digit_count = len(column[0])
        operands = []

        # Go digit by digit to form the numbers
        for digit_index in range(operand_digit_count):
            value = 0

            # Go through each row (in the column) to build the numbers
            for column_row_index in range(len(column)):
                column_value_str = column[column_row_index][digit_index]
                if column_value_str == 'x':
                    continue

                column_value = int(column_value_str)
                # print(f"Column value: {column_value}. Current value: {value}")
                value = (column_value + (value * 10))
                
            operands.append(value)

            # print(f"Operand {digit_index}: {value}")
        sum += reduce(lambda x, y: x + y if operator == '+' else x * y, operands)        

    return sum

if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_6_input.txt")
    #print(f"Part 1: Result: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_6_input.txt")
    print(f"Part 2: Result: {part_2_result}")