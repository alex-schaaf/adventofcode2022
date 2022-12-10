from dataclasses import dataclass
from typing import Literal
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]

# clock circuit ticks at constant rate
# each tick is called a cycle

# CPU with single register X, starting with value 1
# supports 2 instructions
# 1 - addx V, takes 2 cycles, afterwards X register is increased by value V (can be negative)
# 2 - noop, takes 1 cycle, no other effect


@dataclass
class Instruction:
    cmd: Literal["noop", "addx"]
    cycles: int
    value: int | None


instructions: list[Instruction] = []
for line in lines:
    if line == "noop":
        instructions.append(Instruction(line, 1, None))
    elif line.startswith("addx"):
        instruction, value = line.split()
        instructions.append(Instruction(instruction, 2, int(value)))

instructions += [Instruction("noop", 0, None)]
instructions.reverse()


current_instruction = None
current_subcycle = 0
register = 1
cycle = 1


signal_strength_sum = 0
while instructions:
    if not current_instruction:
        current_instruction = instructions.pop()

    logging.debug(
        f"{cycle} | {register:03d} | {current_instruction.cmd} | {current_instruction.value or ''}"
    )

    if current_instruction.cycles > 1:
        cycle += 1
        current_instruction.cycles -= 1
    else:
        cycle += 1
        if current_instruction.value:
            register += current_instruction.value
        logging.debug("--- instruction completed ---")
        current_instruction = None

    if cycle == 20 or (cycle - 20) % 40 == 0:
        signal_strength = cycle * register
        signal_strength_sum += signal_strength
        logging.info(f"{cycle:03d} | {signal_strength}")

print(f"Puzzle 1: {signal_strength_sum}")
