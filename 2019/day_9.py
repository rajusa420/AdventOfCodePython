from intcode_machine import intcode_machine


def do_part_1(file_path):
    program = ""
    with open(file_path, "r") as file:
        for line in file:
            program += line.strip()

    machine = intcode_machine()
    return machine.execute_program(program=program, inputs=[2]) 

if __name__ == "__main__":
    part_1_result = do_part_1("2019/input/day_9_input.txt")
    print(f"{part_1_result}")