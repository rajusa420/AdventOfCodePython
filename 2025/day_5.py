def do_part_1(file_path="day_5_input.text"):
    ids = []
    valid_ranges = []
    with open(file_path, "r") as file:
        for line in file:
            if "-" in line:
                start, end = map(int, line.strip().split("-"))
                valid_ranges.append((start, end))
            elif len(line.strip()) > 0:
                ids.append(int(line.strip()))
    
    valid_ingredients = 0
    for id in ids:
        for start, end in valid_ranges:
            if start <= id <= end:
                valid_ingredients += 1
                break

    return valid_ingredients

def merge_ranges(ranges):
    # First sort the ranges by start
    sorted_ranges = sorted(ranges, key=lambda x: x[0])

    merge_ranges = []
    current_start, current_end = sorted_ranges[0]
    for next_start, next_end in sorted_ranges[1:]:
        if next_start <= current_end:
            # This handles completely contained and overlapping ranges
            current_end = max(current_end, next_end)
        else:
            # No overlap, add the current range and move to next
            merge_ranges.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    # Add the last range
    merge_ranges.append((current_start, current_end))

    return merge_ranges

def count_ranges(merged_ranges):
    return sum(end - start + 1 for start, end in merged_ranges)

def do_part_2(file_path="day_5_input.text"):
    valid_ranges = []
    with open(file_path, "r") as file:
        for line in file:
            if "-" in line:
                start, end = map(int, line.strip().split("-"))
                valid_ranges.append((start, end))
    
    merged_ranges = merge_ranges(valid_ranges)
    #print(f"Merged Ranges: {merged_ranges}")

    total_valid = count_ranges(merged_ranges)
    return total_valid

if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_5_input.txt")
    #print(f"Part 1 Result: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_5_input.txt")
    print(f"Part 2 Result: {part_2_result}")