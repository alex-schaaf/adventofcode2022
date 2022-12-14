from collections import namedtuple, defaultdict
from enum import Enum
from typing import Generator
from copy import deepcopy

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]

Point = namedtuple("Point", "x y")


class Tile(str, Enum):
    Empty = "."
    Rock = "#"
    Sand = "o"
    FallingSand = "~"


def parse_lines(lines: list[str]) -> list[list[Point]]:
    rock_lines = []
    for line in lines:
        rock_line = []
        for coords in line.split(" -> "):
            x, y = coords.split(",")
            rock_line.append(Point(int(x), int(y)))
        rock_lines.append(rock_line)
    return rock_lines


rock_lines = parse_lines(lines)

points = [p for rock_line in rock_lines for p in rock_line]

xs = [p.x for p in points]
ys = [p.y for p in points]


minX, maxX = min(xs), max(xs)
minY, maxY = min(ys), max(ys)


def paint(world: dict[Point, Tile]) -> None:
    # print("    ", end="")
    # for x in range(20):
    #     print(x, end=" ")
    # print("")
    # print("   " + "".join(["--" for _ in range(10)]))
    for y in range(10 + 2):
        # print(y, end=" | ")
        for x in range(20):
            tile = world[Point(x + 489, y)]
            print(tile.value, end=" ")
        print("")


print(f"\n{minX=} {maxX=} {minY=} {maxY=}\n")

world: dict[Point, Tile] = defaultdict(lambda: Tile.Empty)

# populate world with rocks
for rock_line in rock_lines:
    for p1, p2 in zip(rock_line[:-1], rock_line[1:]):
        x1, x2 = sorted([p1.x, p2.x])
        y1, y2 = sorted([p1.y, p2.y])
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                world[Point(x, y)] = Tile.Rock


def get_next_point(point: Point) -> Generator[Point, None, None]:
    for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
        yield Point(point.x + dx, point.y + dy)


def simulate(
    world: dict[Point, Tile], y_offset: int = 0
) -> tuple[dict[Point, Tile], int]:
    simulating = True
    grains = 0
    while simulating:
        sand_start = Point(500, 0)
        blocked = False

        current_point = sand_start
        while not blocked:
            for next_point in get_next_point(current_point):
                if world[next_point] in [Tile.Rock, Tile.Sand]:
                    # print(next_point, "is blocked")
                    continue  # is blocked
                else:
                    # print(next_point, "is free")
                    if next_point.y > maxY + y_offset + 1:
                        simulating = False
                        blocked = True
                        break
                    current_point = next_point
                    break
            else:  # all are blocked
                # deposit sand
                if current_point.x == 500 and current_point.y == 0:
                    simulating = False
                world[current_point] = Tile.Sand
                # print(current_point, "deposited sand")
                blocked = True

        grains += 1
    return world, grains


simulated_world, grains = simulate(deepcopy(world))

print(f"\nPuzzle 1: {grains - 1}")


for x in range(-1000, 1000):
    world[Point(x, maxY + 2)] = Tile.Rock

simulated_world, grains = simulate(world, y_offset=2)
print(f"\nPuzzle 2: {grains}")
