
def do_part_2(file_path="2019/input/day_1_input.txt"):
    total_sum = 0
    with open(file_path, "r") as file:
        for line in file:
            number = int(line.strip())
            fuel = (number // 3) - 2
            line_sum = fuel
            while fuel > 0:
                fuel = (fuel // 3) - 2
                if fuel > 0:
                    line_sum += fuel
            total_sum += line_sum

    return total_sum

def do_part_1(file_path="2019/input/day_1_input.txt"):
    sum = 0
    with open(file_path, "r") as file:
        for line in file:
            number = int(line.strip())
            sum += (number // 3) - 2
    return sum

if __name__ == "__main__":
    result = do_part_1()
    print(result)

    result_2 = do_part_2()
    print(result_2)