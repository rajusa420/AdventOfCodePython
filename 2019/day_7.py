from intcode_machine import intcode_machine
from itertools import permutations

def do_part_1(file_path):
    program = ""
    with open(file_path, "r") as file:
        for line in file:
            program += line.strip()
    
    print(f"Program: {program}")

    phase_setting_options = [0, 1 , 2, 3, 4]
    
    phase_settings_for_max = []
    max_output = 0
    machine = intcode_machine()

    for phase_settings in permutations(phase_setting_options):
        current_input_signal = 0

        for setting in phase_settings:
            inputs = [setting, current_input_signal]
            outputs = machine.execute_program(program, inputs=inputs)
            current_input_signal = outputs.pop()

        if current_input_signal > max_output:
            phase_settings_for_max = phase_settings
            max_output = current_input_signal

    print(f"Max: {max_output} - Phase Settings: {phase_settings_for_max}")
    return max_output

def do_part_2(file_path):
    program = ""
    with open(file_path, "r") as file:
        for line in file:
            program += line.strip()
    
    print(f"Program: {program}")

    phase_setting_options = [5, 6 , 7, 8, 9]
    max_output = 0
    max_output_phase_settings = []

    for phase_settings in permutations(phase_setting_options):
        current_input_signal = 0
        current_index = 0
        current_count = 0
       
        amplifiers = []
        amplifiers_outputs = []

        for index in range(len(phase_setting_options)):
            machine = intcode_machine()
            machine.load_program(program=program)
            amplifiers.append(machine)
            amplifiers_outputs.append([])
       
        while current_input_signal != None:
            current_index = (current_count) % len(phase_settings)
            
            setting = phase_settings[current_index]
            machine = amplifiers[current_index]

            if current_count > len(phase_settings) - 1:
                previous_index = current_index - 1 if current_index > 0 else len(phase_settings) - 1
                inputs = amplifiers_outputs[previous_index]
            else:
                inputs = [setting, current_input_signal]
            
            print(f"Count: {current_count} - Input: {inputs}")
            outputs = machine.resume_execution(inputs=inputs, pause_on_output=True)
            
            if len(outputs) == 0:
                print(f"Outputs was empty!")
                break
            else:
                output = outputs.pop()
                current_input_signal = output
                amplifiers_outputs[current_index] = [output]
                
                print(f"Count: {current_count} - Output: {output}")

            current_count += 1

        final_output = amplifiers_outputs.pop().pop()
        if final_output > max_output:
            max_output = final_output
            max_output_phase_settings = [phase_settings]
            
    print(f"Phase Setting: {max_output_phase_settings} - {max_output}")
    return max_output


if __name__ == "__main__":
    # result = do_part_1("2019/input/day_7_input.txt")
    result = do_part_2("2019/input/day_7_input.txt")
    print(f"Final output: {result}")