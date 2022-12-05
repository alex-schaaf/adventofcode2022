from copy import deepcopy

filename = "./input"

with open(filename, "r") as file:
    lines = [l.rstrip("\n") for l in file.readlines()]


i_split = lines.index("")

stack_lines = lines[: i_split - 1]

stack_numbers = [int(c) for c in lines[i_split - 1].split()]
n_stacks = len(stack_numbers)


stacks = [[] for _ in range(n_stacks)]
for line in stack_lines:
    for s in range(n_stacks):
        crate = line[s * 4 + 1]
        if crate == " ":
            continue
        stacks[s].append(crate)

stacks = [stack[::-1] for stack in stacks]

stacks2 = deepcopy(stacks)

move_lines = lines[i_split + 1 :]

moves = []
for line in move_lines:
    _, n, _, src, _, dst = line.split()
    moves.append((int(n), int(src) - 1, int(dst) - 1))

for (n, src, dst) in moves:
    for _ in range(n):
        crate = stacks[src].pop()
        stacks[dst].append(crate)


message = "".join([stack[-1] for stack in stacks])
print(f"Puzzle 1: {message}")

for (n, src, dst) in moves:
    crates = []
    for _ in range(n):
        crate = stacks2[src].pop()
        crates.append(crate)

    stacks2[dst] = stacks2[dst] + crates[::-1]

message = "".join([stack[-1] for stack in stacks2])
print(f"Puzzle 2: {message}")
