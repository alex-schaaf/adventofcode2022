from string import ascii_lowercase, ascii_uppercase

priorities = ascii_lowercase + ascii_uppercase

filename = "./input"

with open(filename, "r") as file:
    lines = file.readlines()
rucksacks = [line.strip() for line in lines]


priorities_sum = 0
for rucksack in rucksacks:
    middle = len(rucksack) // 2
    c1 = rucksack[:middle]
    c2 = rucksack[middle:]

    inter = set(c1).intersection(c2)

    priority = priorities.index(inter.pop()) + 1
    priorities_sum += priority

print(f"Puzzle 1: {priorities_sum}")


priorities_sum = 0
for i in range(0, len(rucksacks), 3):
    group_rucksacks = rucksacks[i : i + 3]

    badge = (
        set(group_rucksacks[0])
        .intersection(group_rucksacks[1])
        .intersection(group_rucksacks[2])
    )
    priority = priorities.index(badge.pop()) + 1
    priorities_sum += priority

print(f"Puzzle 2: {priorities_sum}")
