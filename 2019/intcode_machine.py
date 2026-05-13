from enum import IntEnum
from dataclasses import dataclass, field
import sys

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
        RELATIVE_BASE_OFFSET = 9
        HALT = 99

    class ParameterMode(IntEnum):
        POSITION = 0
        IMMEDIATE = 1
        RELATIVE = 2

    @dataclass
    class Parameter:
        instruction_param: int
        mode: intcode_machine.ParameterMode

    def __init__(self):
        self.instruction_pointer = 0
        self.memory = []
        self.debugInstructionLogging = False
        self.relative_base_pointer = 0

    def get_parameter_count(self, opcode):
        match opcode:
            case self.Opcode.ADD | self.Opcode.MULTIPLY | self.Opcode.LESS_THAN | self.Opcode.EQUALS:
                return 3
            case self.Opcode.JUMP_IF_TRUE | self.Opcode.JUMP_IF_FALSE:
                return 2
            case self.Opcode.INPUT | self.Opcode.PRINT | self.Opcode.RELATIVE_BASE_OFFSET:
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
                dest = self.resolve_destination_parameter(param3)
                self.set_memory(dest, str(val1 + val2))
                if self.debugInstructionLogging:
                    print(f"ADD: {val1} + {val2} -> {dest}")

            case self.Opcode.MULTIPLY:
                param1, param2, param3 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                dest = self.resolve_destination_parameter(param3)

                self.set_memory(dest, str(val1 * val2))
                if self.debugInstructionLogging:
                    print(f"MULTIPLY: {val1} * {val2} -> {dest}")

            case self.Opcode.INPUT:
                param = parameters[0]
                dest = self.resolve_destination_parameter(param)
                input_string = self.getNextInput()
                self.set_memory(dest, input_string)
                if self.debugInstructionLogging:
                    print(f"INPUT: {input_string} -> {dest}")

            case self.Opcode.PRINT:
                param = parameters[0]
                val1 = self.resolve_parameter(param)
                #print(f"{val1}")
                self.outputs.append(val1)
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
                dest = self.resolve_destination_parameter(param3)
                self.set_memory(dest, str(1) if val1 < val2 else str(0))

            case self.Opcode.EQUALS:
                param1, param2, param3 = parameters
                val1 = self.resolve_parameter(param1)
                val2 = self.resolve_parameter(param2)
                dest = self.resolve_destination_parameter(param3)
                self.set_memory(dest, str(1) if val1 == val2 else str(0))

            case self.Opcode.RELATIVE_BASE_OFFSET:
                param = parameters[0]
                val1 = self.resolve_parameter(param)
                self.relative_base_pointer += val1

                if self.debugInstructionLogging:
                    print(f"RELATIVE_BASE_OFFSET: {self.relative_base_pointer}")

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
                return int(self.get_memory(parameter.instruction_param))
            case self.ParameterMode.RELATIVE: 
                return int(self.get_memory(self.relative_base_pointer + parameter.instruction_param))
            case self.ParameterMode.IMMEDIATE:
                return parameter.instruction_param
    
    def resolve_destination_parameter(self, parameter: intcode_machine.Parameter):
        match parameter.mode:
            case self.ParameterMode.POSITION:
                return parameter.instruction_param
            case self.ParameterMode.RELATIVE:
                return self.relative_base_pointer + parameter.instruction_param
            case self.ParameterMode.IMMEDIATE:
                sys.exit("Unexpected parameter mode for destination param")
            
    def getNextInput(self):
        if self.inputs is not None:
            return str(self.inputs.pop(0))
        else:
            input_string = input("Input: ")
            return input_string

    def load_memory(self, memory):
        self.memory = memory

    def set_memory(self, pointer, value):
        if pointer >= len(self.memory):
            self.memory.extend(["0"] * (pointer - len(self.memory) + 1))
        self.memory[pointer] = value

    def get_memory(self, pointer):
        if pointer >= len(self.memory):
            return 0

        return self.memory[pointer]

    def load_program(self, program):
        memory = program.split(",")
        self.load_memory(memory=memory)

    def execute_program(self, program, inputs=None):
        memory = program.split(",")
        return self.execute(memory, inputs)
    
    def resume_execution(self, inputs=None, pause_on_output=False):
        return self.execute(memory_input=self.memory, inputs=inputs, instruction_pointer=self.instruction_pointer, pause_on_output=pause_on_output)

    def execute(self, memory_input, inputs=None, instruction_pointer=0, pause_on_output=False):
        self.load_memory(memory=memory_input)
        self.inputs = inputs
        self.outputs = []
        self.instruction_pointer = instruction_pointer

        while self.instruction_pointer >= 0:
            instruction = self.get_memory(self.instruction_pointer)
            if self.debugInstructionLogging:
                print(f"Instruction: {instruction}")
    
            opcode, parameter_mode_list = self.parse_instruction(instruction=instruction)

            parameter_count = self.get_parameter_count(opcode)

            if self.debugInstructionLogging:
                instruction_parameters_strings = [self.get_memory(self.instruction_pointer + i + 1) for i in range(parameter_count)]
                print(f"Parameters: {instruction_parameters_strings}")
            instruction_parameters = [int(self.get_memory(self.instruction_pointer + i + 1)) for i in range(parameter_count)]
            parameters = [self.Parameter(instruction_parameters[i], parameter_mode_list[i] if i < len(parameter_mode_list) else self.ParameterMode.POSITION) for i in range(parameter_count)]

            original_instruction_pointer = self.instruction_pointer
            self.handle_opcode(opcode, parameters)

            # if handling the instruction moved the ip then we continue processing from there
            if self.instruction_pointer == original_instruction_pointer:
                self.instruction_pointer += (parameter_count + 1)

            if pause_on_output and opcode == self.Opcode.PRINT:
                return self.outputs
        
        return self.outputs

