from intcode_machine import intcode_machine

def do_part_2(file_path="2019/input/day_2_input.txt"):
    program = ""
    with open(file_path, "r") as file:
        for line in file:
            program += line.strip()

    original_memory = program.split(",")
    for noun in range(100):
        for verb in range(100):
            memory = original_memory.copy()
            memory[1] = str(noun)
            memory[2] = str(verb)

            machine = intcode_machine()
            result_memory = machine.execute(memory)

            if int(result_memory[0]) == 19690720:
                print(f"Found noun={noun}, verb={verb}")
                return 100 * noun + verb
        

def do_part_1(file_path="2019/input/day_2_input.txt"):
    program = ""
    with open(file_path, "r") as file:
        for line in file:
            program += line.strip()

    memory = program.split(",")
    memory[1] = "12"
    memory[2] = "2"

    machine = intcode_machine()
    result_memory = machine.execute(memory)
    
    return int(result_memory[0])

if __name__ == "__main__":
    result = do_part_1(file_path="2019/input/day_2_input.txt")
    print(result)

    result_2 = do_part_2(file_path="2019/input/day_2_input.txt")
    print(result_2)