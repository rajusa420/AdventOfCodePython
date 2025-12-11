from dataclasses import dataclass, field
import numpy as np
from z3 import *

@dataclass
class Machine:
    final_light_state: str = ''
    wiring_schemes: list = field(default_factory=list)
    wiring_matrix_list: list = field(default_factory=list)
    joltage: list = field(default_factory=list)

def process_machine_1(machine: Machine):
    number_of_lights = len(machine.final_light_state)
    current_light_state = '.' * number_of_lights

    def apply_scheme(current_state, scheme):
        updated_state = list(current_state)
        for index in scheme:
            if updated_state[index] == '.':
                updated_state[index] = '#'
            else:
                updated_state[index] = '.'
        return ''.join(updated_state)
    
    # current, final, schemes, presses
    processed_states = set()
    queue = [(current_light_state, machine.final_light_state, machine.wiring_schemes, 0)]
    while queue:
        current_state, final_state, schemes, presses = queue.pop(0)

        for scheme in schemes:
            new_state = apply_scheme(current_state, scheme)
            if new_state == final_state:
                return presses + 1
            
            if new_state not in processed_states:
                processed_states.add(new_state)
                queue.append((new_state, final_state, schemes, presses + 1))
    
    raise Exception("No solution found")

def process_file(file_path="day_10_input.txt"):
    machines = []
    with open(file_path, "r") as file:
        for line in file:
            line_parts = line.strip().split(" ")

            final_light_state = ''
            wiring_schemes = []
            wiring_matrix_list = []
            joltage = []
            for line_part in line_parts:
                first_char = line_part[0]
                if first_char == '[':
                    final_light_state = line_part[1:-1]
                elif first_char == '(':
                    scheme = list(map(int, line_part[1:-1].split(",")))
                    wiring_schemes.append(scheme)
                    # Create wiring matrix
                    number_of_lights = len(final_light_state)
                    wiring_matrix = np.array([0 for _ in range(number_of_lights)])
                    for index in scheme:
                        wiring_matrix[index] = 1
                    wiring_matrix_list.append(wiring_matrix)

                else:
                    joltage = list(map(int, line_part[1:-1].split(",")))

            machine = Machine(final_light_state=final_light_state, wiring_schemes=wiring_schemes, wiring_matrix_list=wiring_matrix_list, joltage=joltage)
            machines.append(machine)
    return machines

def do_part_1(file_path="day_10_input.txt"):
    machines = process_file(file_path)
    sum_of_presses = 0
    for machine in machines:
        sum_of_presses += process_machine_1(machine)
    
    return sum_of_presses

def process_machine_2(machine: Machine):
    number_of_lights = len(machine.final_light_state)
    current_light_state_matrix = np.zeros(number_of_lights, dtype=int)
    joltage_matrix = np.array(machine.joltage)

    def apply_scheme(current_state, scheme_matrix):
        return current_state + scheme_matrix

    queue = [(current_light_state_matrix, machine.wiring_matrix_list, 0)]
    processed_states = set()
    while queue:
        current_state_matrix, wiring_matrix_list, presses = queue.pop(0)

        for wiring_matrix in wiring_matrix_list:
            new_state = apply_scheme(current_state_matrix, wiring_matrix)

            # Check if all values match joltage
            if np.array_equal(new_state, joltage_matrix):
                return presses + 1

            # If any value exceeds joltage, skip this state
            if np.any(new_state > joltage_matrix):
                continue

            state_tuple = tuple(new_state)
            if state_tuple not in processed_states:
                processed_states.add(state_tuple)
                queue.append((new_state, wiring_matrix_list, presses + 1))

    raise Exception("No solution found")

def process_machine_2_v2(machine: Machine):
    number_of_lights = len(machine.final_light_state)
    joltage_matrix = np.array(machine.joltage)
    wiring_matrix_list = machine.wiring_matrix_list

    best_presses = float('inf')
    # Track the best (lowest) press count to reach each state
    state_best_presses = {}

    def dfs(current_state, presses):
        nonlocal best_presses

        # Prune if we've already used more presses than best solution
        if presses >= best_presses:
            return

        for wiring_matrix in wiring_matrix_list:
            new_state = current_state + wiring_matrix
            new_presses = presses + 1

            # Check if all values match joltage
            if np.array_equal(new_state, joltage_matrix):
                if new_presses < best_presses:
                    best_presses = new_presses
                    print(f"  Found solution with {best_presses} presses")
                continue

            # If any value exceeds joltage, skip this state
            if np.any(new_state > joltage_matrix):
                continue

            # Prune if we've reached this state with fewer presses before
            state_tuple = tuple(new_state)
            if state_tuple in state_best_presses and state_best_presses[state_tuple] <= new_presses:
                continue
            state_best_presses[state_tuple] = new_presses

            dfs(new_state, new_presses)

    initial_state = np.zeros(number_of_lights, dtype=int)
    dfs(initial_state, 0)

    if best_presses == float('inf'):
        raise Exception("No solution found")
    return best_presses

# Used AI to build the recommended solution from reddit via Z3 solver
def process_machine_2_v3(machine: Machine):
    """Use Z3 solver to find minimum button presses."""
    num_schemes = len(machine.wiring_schemes)
    num_lights = len(machine.joltage)
    joltage = machine.joltage

    # Create Z3 integer variables for how many times each button is pressed
    presses = [Int(f'p{i}') for i in range(num_schemes)]

    optimizer = Optimize()

    # Each press count must be non-negative
    for p in presses:
        optimizer.add(p >= 0)

    # For each light position, sum of (presses * scheme contribution) must equal joltage
    for light_idx in range(num_lights):
        total = Sum([presses[scheme_idx] * (1 if light_idx in machine.wiring_schemes[scheme_idx] else 0) for scheme_idx in range(num_schemes)])
        optimizer.add(total == joltage[light_idx])

    # Minimize total button presses
    optimizer.minimize(Sum(presses))

    if optimizer.check() == sat:
        model = optimizer.model()
        total_presses = sum(model[p].as_long() for p in presses)
        return total_presses
    else:
        raise Exception("No solution found")

def do_part_2(file_path="day_10_input.txt"):
    machines = process_file(file_path)
    sum_of_presses = 0
    for machine in machines:
        presses = process_machine_2_v3(machine)
        print(f"Machine with final state {machine.final_light_state} and joltage {machine.joltage} requires {presses} presses")
        sum_of_presses += presses
    
    return sum_of_presses
    
if __name__ == "__main__":
    #part_1_result = do_part_1("2025/input/day_10_input.txt")
    #print(f"Part 1: Result: {part_1_result}")

    part_2_result = do_part_2("2025/input/day_10_input.txt")
    print(f"Part 2: Result: {part_2_result}")