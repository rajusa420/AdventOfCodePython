def process_line(line, total_digits):
    line_length = len(line)
    previous_max_index = -1
    max_digits = []
    for current_digit in range(total_digits, 0, -1):
        max_value_for_current_digit = -1
        for index in range(previous_max_index + 1, line_length - (current_digit - 1)):
            digit = int(line[index])
            if digit > max_value_for_current_digit:
                max_value_for_current_digit = digit
                previous_max_index = index
        max_digits.append(max_value_for_current_digit)
    
    joltage = 0
    power = 0
    for digit in reversed(max_digits):
        joltage += digit * (10 ** power)
        power += 1
    return joltage

def process_file(file_path="day_3_input.txt", total_digits=2):
    joltage = 0
    with open(file_path, "r") as file:
        for line in file:
            line_joltage = process_line(line.strip(), total_digits)
            #print(f"Line: {line} - Joltage: {line_joltage}")
            joltage += line_joltage

    return joltage

if __name__ == "__main__":
    part_1_joltage = process_file("2025/input/day_3_input.txt", 2)
    print(f"Part 1: Final joltage: {part_1_joltage}")

    part_2_joltage = process_file("2025/input/day_3_input.txt", 12)
    print(f"Part 2: Final joltage: {part_2_joltage}")