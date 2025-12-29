from enum import IntEnum

class intcode_machine:
    class Opcode(IntEnum):
        ADD = 1
        MULTIPLY = 2
        HALT = 99

    def __init__(self):
        self.instruction_pointer = 0
        self.memory = []
        self.debugInstructionLogging = True

    def get_parameter_count(self, opcode):
        match opcode:
            case self.Opcode.ADD | self.Opcode.MULTIPLY:
                return 3
            case self.Opcode.HALT:
                return 0
            case _:
                raise Exception(f"Unknown opcode: {opcode}")
            
    def handle_opcode(self, opcode, parameters):
        match opcode:
            case self.Opcode.ADD:
                src1, src2, dest = parameters
                val1 = int(self.memory[src1])
                val2 = int(self.memory[src2])
                self.memory[dest] = str(val1 + val2)
                if self.debugInstructionLogging:
                    print(f"ADD: {val1} + {val2} -> {self.memory[dest]}")

            case self.Opcode.MULTIPLY:
                src1, src2, dest = parameters
                val1 = int(self.memory[src1])
                val2 = int(self.memory[src2])
                self.memory[dest] = str(val1 * val2)
                if self.debugInstructionLogging:
                    print(f"MULTIPLY: {val1} * {val2} -> {self.memory[dest]}")

            case self.Opcode.HALT:
                self.instruction_pointer = -999999

            case _:
                raise Exception(f"Unknown opcode: {opcode}")

    def execute(self, memory_input):
        self.memory = memory_input
        self.instruction_pointer = 0

        while self.instruction_pointer >= 0:
            opcode = int(self.memory[self.instruction_pointer])
            parameter_count = self.get_parameter_count(opcode)
            parameters = [int(self.memory[self.instruction_pointer + i + 1]) for i in range(parameter_count)]
            self.handle_opcode(opcode, parameters)
            self.instruction_pointer += (parameter_count + 1)
        
        return self.memory

