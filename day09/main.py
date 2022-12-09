from dataclasses import dataclass
from enum import Enum

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


commands: list[tuple[str, int]] = []
for line in lines:
    direction, steps = line.split()
    commands.append((direction, int(steps)))


class Direction(str, Enum):
    UP = "U"
    RIGHT = "R"
    DOWN = "D"
    LEFT = "L"


@dataclass
class Point:
    x: int
    y: int

    def move_direction(self, direction: Direction) -> None:
        match direction:
            case Direction.UP:
                self.y += 1
            case Direction.RIGHT:
                self.x += 1
            case Direction.DOWN:
                self.y -= 1
            case Direction.LEFT:
                self.x -= 1
            case _:
                raise ValueError("Invalid direction")


def chebyshev_components(point_a: Point, point_b: Point) -> tuple[int]:
    """Get x and y components for Chebyshev distance"""
    return (point_a.x - point_b.x, point_a.y - point_b.y)


def get_distance(point_a: Point, point_b: Point) -> int:
    """Chebyshev distance between head and tail"""
    dx, dy = chebyshev_components(point_a, point_b)
    return max((abs(dx), abs(dy)))


def are_diagonal(point_a: Point, point_b: Point) -> bool:
    """Check if head and tail are in diagonal arrangement"""
    dx, dy = chebyshev_components(point_a, point_b)
    return all((dx, dy))


head = Point(0, 0)
tail = Point(0, 0)
tail_visited: set[tuple[int]] = set((0, 0))

for (direction, steps) in commands:
    for step in range(steps):
        head.move_direction(direction)
        if get_distance(head, tail) > 1:
            dx, dy = chebyshev_components(head, tail)
            tail.x += int(dx / (abs(dx) or 1))
            tail.y += int(dy / (abs(dy) or 1))
            tail_visited.add((tail.x, tail.y))


print(f"Puzzle 1: {len(tail_visited)}")


head = Point(0, 0)
knots = [Point(0, 0) for _ in range(9)]
tail_visited: set[tuple[int]] = set()


for n_step, (direction, steps) in enumerate(commands):
    for step in range(steps):
        head.move_direction(direction)
        for i, (knot_a, knot_b) in enumerate(
            zip([head, *knots][:-1], [head, *knots][1:])
        ):
            distance = get_distance(knot_a, knot_b)
            if distance > 1:
                dx, dy = chebyshev_components(knot_a, knot_b)
                knot_b.x += int(dx / (abs(dx) or 1))
                knot_b.y += int(dy / (abs(dy) or 1))

            if i == len(knots) - 1:
                tail_visited.add((knot_b.x, knot_b.y))


print(f"Puzzle 2: {len(tail_visited)}")
