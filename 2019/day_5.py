from intcode_machine import intcode_machine

def do_part_1(file_path):
    program = ""
    with open(file_path, "r") as file:
        for line in file:
            program += line.strip()
    
    print(f"Program: {program}")

    machine = intcode_machine()
    result_memory = machine.execute_program(program)

    return 0

if __name__ == "__main__":
    do_part_1("2019/input/day_5_input.txt")