from dataclasses import dataclass
from typing import Literal
import logging
from pprint import pprint

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

print("\n")

current_instruction = None
current_subcycle = 0
X = 1
cycle = 1
signal_strength_sum = 0
sprite_size = 3
crt_width = 40
crt_height = 6

screen = [["." for _ in range(crt_width)] for _ in range(crt_height)]

current_row = -1

screen = [[]]

while instructions:
    if not current_instruction:
        current_instruction = instructions.pop()

    logging.debug(
        f"{cycle} | {X:03d} | {current_instruction.cmd} | {current_instruction.value or ''}"
    )

    # if cycle > 21:
    #     break

    if cycle == 1 or (cycle - 1) % 40 == 0:
        screen.append([])
        if cycle > 240:
            break
        current_row += 1
        # print(f"{cycle:03d} | {current_row}")

    current_pixel_x = (cycle % 40) - 1
    current_pixel_y = current_row
    current_sprite_pos = X

    if current_pixel_x - 1 <= X <= current_pixel_x + 1:
        screen[current_row].append("#")
    else:
        screen[current_row].append(".")

    a = ["." for _ in range(crt_width)]

    if X > 0:
        a[X - 1] = "#"
    a[X] = "#"
    try:
        a[X + 1] = "#"
    except IndexError:
        pass
    # print(f"{cycle:02d} {''.join(a)}")

    # print(
    #     f"Start cycle {cycle:03d}: begin executing {current_instruction.cmd} {current_instruction.value}"
    # )

    # print("   " + "".join(screen[current_row]) + f"  {X=} {cycle=}")
    # print("")

    if current_instruction.cycles > 1:
        cycle += 1
        current_instruction.cycles -= 1
    else:
        cycle += 1
        if current_instruction.value:
            X += current_instruction.value
        logging.debug("--- instruction completed ---")
        current_instruction = None

    if cycle == 20 or (cycle - 20) % 40 == 0:
        signal_strength = cycle * X
        signal_strength_sum += signal_strength
        logging.debug(f"{cycle:03d} | {signal_strength}")


print(f"Puzzle 1: {signal_strength_sum}")
print("")
for row in screen:
    print("".join(row))
