from collections import defaultdict, namedtuple
from enum import Enum
from operator import attrgetter
from string import digits
from typing import Literal

Loc = namedtuple("Loc", "x y")


class Tile(str, Enum):
    GROUND = "."
    WALL = "#"


def parse_path(path_str: str) -> list[int | Literal["L", "R"]]:
    commands = []
    number = ""
    for c in path_str:
        if c in digits:
            number += c
        else:
            commands.append(int(number))
            number = ""
            commands.append(c)
    commands.append(int(number))
    return commands


def parse_map(lines: list[str]) -> tuple[dict[Loc, str], Loc]:
    world = {}
    start = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == " ":
                continue
            else:
                if not start and c == ".":
                    start = Loc(x, y)
                world[Loc(x, y)] = c
    return world, start


def rotate(direction: int, command: Literal["L", "R"]) -> int:
    if command == "L":
        return (direction - 90) % 360
    elif command == "R":
        return (direction + 90) % 360
    else:
        raise ValueError("Invalid direction")


def move(
    current: Loc,
    steps: int,
    direction: int,
    world: defaultdict[Loc, str],
) -> Loc:
    dx, dy = {0: (0, -1), 90: (1, 0), 180: (0, 1), 270: (-1, 0)}[direction]
    for _ in range(steps):
        loc = Loc(current.x + dx, current.y + dy)

        if world.get(loc) is None:
            if direction == 0:
                loc = max(
                    filter(lambda location: location.x == current.x, world.keys()),
                    key=attrgetter("y"),
                )
            elif direction == 90:
                loc = min(
                    filter(lambda location: location.y == current.y, world.keys()),
                    key=attrgetter("x"),
                )
            elif direction == 180:
                loc = min(
                    filter(lambda location: location.x == current.x, world.keys()),
                    key=attrgetter("y"),
                )
            elif direction == 270:
                loc = max(
                    filter(lambda location: location.y == current.y, world.keys()),
                    key=attrgetter("x"),
                )

        if world[loc] == "#":
            break
        else:
            current = loc
    return current


if __name__ == "__main__":
    filepath = "./input.txt"

    with open(filepath, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    path = parse_path(lines[-1])
    world, start = parse_map(lines[:-1])
    print(f"{start=}")

    direction = 90
    current = Loc(start.x, start.y)

    for command in path:
        if isinstance(command, int):
            current = move(current, command, direction, world)
        elif command in ("L", "R"):
            direction = rotate(direction, command)
        else:
            raise ValueError("Invalid command")

    print(current, direction)

    result = (
        1000 * (current.y + 1)
        + 4 * (current.x + 1)
        + {90: 0, 180: 1, 270: 2, 0: 3}[direction]
    )
    print(f"Puzzle 1: {result}")
