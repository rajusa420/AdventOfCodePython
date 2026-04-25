from enum import IntEnum
from dataclasses import dataclass, field

class intcode_machine:
    class Opcode(IntEnum):
        ADD = 1
        MULTIPLY = 2
        INPUT = 3
        PRINT = 4
        JUMP_IF_TRUE = 5
        JUMP_IF_FALSE = 6
        LESS_THAN = 7
        EQUALS = 8
        HALT = 99

    class ParameterMode(IntEnum):
        POSITION = 0
        IMMEDIATE = 1

    @dataclass
    class Parameter:
        instruction_param: int
        mode: intcode_machine.ParameterMode

    def __init__(self):
        self.instruction_pointer = 0
        self.memory = []
        self.debugInstructionLogging = False

    def get_parameter_count(self, opcode):
        match opcode:
            case self.Opcode.ADD | self.Opcode.MULTIPLY | self.Opcode.LESS_THAN | self.Opcode.EQUALS:
                return 3
            case self.Opcode.JUMP_IF_TRUE | self.Opcode.JUMP_IF_FALSE:
                return 2
            case self.Opcode.INPUT | self.Opcode.PRINT:
                return 1
            case self.Opcode.HALT:
                return 0
            case _:
                raise Exception(f"Unknown opcode: {opcode}")
            
    def handle_opcode(self, opcode, parameters):
        match opcode:
            case self.Opcode.ADD:
                param1, param2, param3 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                dest = param3.instruction_param
                self.memory[dest] = str(val1 + val2)
                if self.debugInstructionLogging:
                    print(f"ADD: {val1} + {val2} -> {dest}")

            case self.Opcode.MULTIPLY:
                param1, param2, param3 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                dest = param3.instruction_param

                self.memory[dest] = str(val1 * val2)
                if self.debugInstructionLogging:
                    print(f"MULTIPLY: {val1} * {val2} -> {dest}")

            case self.Opcode.INPUT:
                param = parameters[0]
                dest = param.instruction_param
                input_string = input("Input: ")
                self.memory[dest] = input_string
                if self.debugInstructionLogging:
                    print(f"INPUT: {input_string} -> {dest}")

            case self.Opcode.PRINT:
                param = parameters[0]
                val1 = self.resolve_parameter(param)
                print(f"{val1}")
                if self.debugInstructionLogging:
                    print(f"PRINT: {val1}")

            case self.Opcode.JUMP_IF_TRUE:
                param1, param2 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                if val1 > 0:
                    self.instruction_pointer = val2

            case self.Opcode.JUMP_IF_FALSE:
                param1, param2 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                if val1 == 0:
                    self.instruction_pointer = val2

            case self.Opcode.LESS_THAN:
                param1, param2, param3 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                dest = param3.instruction_param
                self.memory[dest] = 1 if val1 < val2 else 0

            case self.Opcode.EQUALS:
                param1, param2, param3 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                dest = param3.instruction_param
                self.memory[dest] = 1 if val1 == val2 else 0

            case self.Opcode.HALT:
                self.instruction_pointer = -999999

            case _:
                raise Exception(f"Unknown opcode: {opcode}")
            
    def parse_instruction(self, instruction):
        parameter_modes_string, opcode_string = instruction[:-2], instruction[-2:]
        opcode = int(opcode_string)
        parameter_modes_list = [int(parameter_mode) for parameter_mode in parameter_modes_string[::-1]]
        return (opcode, parameter_modes_list)

    def resolve_parameter(self, parameter: intcode_machine.Parameter):
        match parameter.mode:
            case self.ParameterMode.POSITION:
                return int(self.memory[parameter.instruction_param])
            case self.ParameterMode.IMMEDIATE:
                return parameter.instruction_param

    def execute_program(self, program):
        memory = program.split(",")
        return self.execute(memory)

    def execute(self, memory_input):
        self.memory = memory_input
        self.instruction_pointer = 0

        while self.instruction_pointer >= 0:
            instruction = self.memory[self.instruction_pointer]
    
            opcode, parameter_mode_list = self.parse_instruction(instruction=instruction)

            parameter_count = self.get_parameter_count(opcode)
            instruction_parameters = [int(self.memory[self.instruction_pointer + i + 1]) for i in range(parameter_count)]
            parameters = [self.Parameter(instruction_parameters[i], parameter_mode_list[i] if i < len(parameter_mode_list) else self.ParameterMode.POSITION) for i in range(parameter_count)]
            
            original_instruction_pointer = self.instruction_pointer
            self.handle_opcode(opcode, parameters)

            # if handling the instruction moved the ip then we continue processing from there
            if self.instruction_pointer == original_instruction_pointer:
                self.instruction_pointer += (parameter_count + 1)
        
        return self.memory

