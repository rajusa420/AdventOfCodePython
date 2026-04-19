


def do_part_1(file_path):
    range_bottom = 0
    range_top = 0
    with open(file_path, "r") as file:
        for line in file:
            numbers = line.split("-")
            range_bottom = int(numbers[0])
            range_top = int(numbers[1])

    matches = 0
    for number in range(range_bottom, range_top):
        prev_digit = None
        is_match = True
        found_matching_digit = False
        for digit_str in str(number):
            digit = int(digit_str)

            if prev_digit is not None:
                if prev_digit > digit:
                    is_match = False
                    break

                if digit == prev_digit:
                    found_matching_digit = True

            prev_digit = digit
        
        if is_match and found_matching_digit:
            matches += 1

    return matches

def do_part_2(file_path):
    range_bottom = 0
    range_top = 0
    with open(file_path, "r") as file:
        for line in file:
            numbers = line.split("-")
            range_bottom = int(numbers[0])
            range_top = int(numbers[1])

    matches = 0
    for number in range(range_bottom, range_top + 1):
        prev_digit = None
        is_match = True
        found_matching_digit = False
        found_exact_2_match = False
        digit_sequence = ""
        
        for digit_str in str(number):
            digit = int(digit_str)

            if prev_digit is not None:
                if prev_digit > digit:
                    is_match = False
                    break

                if digit == prev_digit:
                    digit_sequence += str(digit)

                    if len(digit_sequence) == 2:
                        found_matching_digit = True
                    else:
                        found_matching_digit = False
                else: 
                    digit_sequence = str(digit)
                    if found_matching_digit:
                        found_exact_2_match = True
                        found_matching_digit = False
            else:
                digit_sequence = str(digit)

            prev_digit = digit
        
        if is_match and (found_exact_2_match or found_matching_digit):
            matches += 1

    return matches

if __name__ == "__main__":
    result = do_part_2(file_path="2019/input/day_4_input.txt")
    print(result)