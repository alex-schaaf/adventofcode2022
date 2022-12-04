filename = "./input"

with open(filename, "r") as file:
    lines = file.readlines()
lines = [line.strip() for line in lines]


containments = 0
overlaps = 0
for line in lines:
    print("")
    elf1, elf2 = line.split(",")
    elf1 = [int(e) for e in elf1.split("-")]
    elf2 = [int(e) for e in elf2.split("-")]

    if (elf1[0] >= elf2[0] and elf1[1] <= elf2[1]) or (
        elf2[0] >= elf1[0] and elf2[1] <= elf1[1]
    ):
        containments += 1

    # visualization
    print(
        "".join(
            ["." for _ in range(0, elf1[0])]
            + ["#" for _ in range(elf1[0], elf1[1] + 1)]
            + ["." for _ in range(elf1[1], 101)]
        )
    )
    print(
        "".join(
            ["." for _ in range(0, elf2[0])]
            + ["#" for _ in range(elf2[0], elf2[1] + 1)]
            + ["." for _ in range(elf2[1], 101)]
        )
    )

    if elf1[1] >= elf2[0] and elf1[0] <= elf2[1]:
        overlaps += 1
        print(elf1, elf2, "OVERLAP!")
    else:
        print(elf1, elf2)


print(f"Puzzle 1: {containments}")
print(f"Puzzle 2: {overlaps}")
