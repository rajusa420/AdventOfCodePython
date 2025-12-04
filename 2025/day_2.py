

def get_sum_of_invalid_ids(start, end):
    sum = 0
    for number in range(start, end + 1):
        str_num = str(number)
        length = len(str_num)
        # Needs to have even number of digits to be invalid
        if length % 2 != 0:
            continue

        half_length = length // 2
        first = str_num[:half_length]
        second = str_num[half_length:]
        if first == second:
            sum += number
    return sum

def do_part_1(file_path="day_1_input.txt"):
    sum = 0
    with open(file_path, "r") as file:
        for line in file:
            ranges = line.strip().split(',')
            for range in ranges:
                numbers = list(map(int, range.split('-')))
                start = numbers[0]
                end = numbers[1]
                sum += get_sum_of_invalid_ids(start, end)
    return sum

def get_sum_of_invalid_ids_part_2(start, end):
    sum = 0
    for number in range(start, end + 1):
        str_num = str(number)
        length = len(str_num)
        half_length = length // 2
        for repeat_size in range(1, half_length + 1):
            # Repeat size has to be a divisor of the length
            if length % repeat_size != 0:
                continue

            # Probably don't need to save the chunks, can just compare
            chunks = []
            for i in range(0, length, repeat_size):
                chunks.append(str_num[i:i+repeat_size])

            test_sequence = chunks.pop(0)
            # Can do:  all_equal = all(chunk == test_sequence for chunk in chunks)
            # all_equal = True
            # for chunk in chunks:
            #    if chunk != test_sequence:
            #        all_equal = False
            #        break
            all_equal = all(chunk == test_sequence for chunk in chunks)
            
            if all_equal:
                sum += number
                break

    return sum

def do_part_2(file_path="day_1_input.txt"):
    sum = 0
    with open(file_path, "r") as file:
        for line in file:
            ranges = line.strip().split(',')
            for range in ranges:
                numbers = list(map(int, range.split('-')))
                start = numbers[0]
                end = numbers[1]
                sum += get_sum_of_invalid_ids_part_2(start, end)
    return sum

if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_2_input.txt")
    #print(f"Part 1 Result: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_2_input.txt")
    print(f"Part 2 Result: {part_2_result}")