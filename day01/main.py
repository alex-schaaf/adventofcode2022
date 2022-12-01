filename = "./input"
elves: list[list[int]] = []

with open(filename, "r") as file:
    current_elf = []
    for line in file.readlines():
        if line == "\n":
            elves.append(current_elf)
            current_elf = []
            continue
        current_elf.append(int(line.strip()))


max = 0
for elf in elves:
    calories = sum(elf)
    if calories > max:
        max = calories

print(f"Puzzle 1: {max}")

sums = []
for elf in elves:
    sums.append(sum(elf))

sums.sort(reverse=True)

print(f"Puzzle 2: {sum(sums[:3])}")
