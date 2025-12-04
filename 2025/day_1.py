def process_line_part(line):
    direction = line[0]
    distance = int(line[1:])

    if direction == 'R':
        return distance
    elif direction == 'L':
        return -distance
    else:
        raise ValueError("Invalid direction")

def do_part_1(file_path="day_1_input.txt"):
    current = 50
    zero_count = 0
    step_index = 0
    with open(file_path, "r") as file:
        for line in file:
            step_index += 1
            
            current += process_line_part(line.strip())
            current = current % 100

            if current == 0:
                zero_count += 1

            #print(f"{step_index} ({line}): Current position: {current} - Zero count: {zero_count}")
    return zero_count
    

def do_part_2(file_path="day_1_input.txt"):
    current = 50
    zero_count = 0
    step_index = 0
    with open(file_path, "r") as file:
        for line in file:
            step_index += 1

            previous = current
            current += process_line_part(line.strip())

            if current > 0:
                zero_count += ((current // 100) + (1 if previous < 0 else 0))
            elif current == 0:
                zero_count += 1
            else:
                zero_count += ((abs(current) // 100) + (1 if previous > 0 else 0))

            current = current % 100
            #print(f"{step_index} ({line}): Current position: {current} - Zero count: {zero_count}")
    return zero_count
    

if __name__ == "__main__":
    zero_count_1 = do_part_1("2025/input/day_1_input.txt")
    print(f"Part 1: Number of times at position 0: {zero_count_1}")

    zero_count_2 = do_part_2("2025/input/day_1_input.txt")
    print(f"Part 2: Number of times at position 0: {zero_count_2}")