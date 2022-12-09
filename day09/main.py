from pprint import pprint
from dataclasses import dataclass
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

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

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


def chebyshev_components(point_a: Point, point_b: Point) -> tuple[int]:
    return (point_a.x - point_b.x, point_a.y - point_b.y)


def get_distance(point_a: Point, point_b: Point) -> int:
    """Chebyshev distance between head and tail"""
    dx, dy = chebyshev_components(point_a, point_b)
    return max((abs(dx), abs(dy)))


def are_diagonal(point_a: Point, point_b: Point) -> bool:
    """Check if head and tail are in diagonal arrangement"""
    dx, dy = chebyshev_components(point_a, point_b)
    return all((dx, dy))


class NaiveRope:
    def __init__(self, x: int, y: int) -> None:
        self.head = Point(x=x, y=y)
        self.tail = Point(x=x, y=y)
        self.tail_visited = set((x, y))

    def move(self, direction: Direction, steps: int) -> None:
        for _ in range(steps):
            self.head.move_direction(direction)
            if get_distance(self.head, self.tail) > 1:
                if are_diagonal(self.head, self.tail):
                    dx, dy = chebyshev_components(self.head, self.tail)
                    self.tail.x += int(dx / abs(dx))
                    self.tail.y += int(dy / abs(dy))
                else:
                    self.tail.move_direction(direction)
                self.tail_visited.add((self.tail.x, self.tail.y))


rope = NaiveRope(0, 0)

for (direction, steps) in commands:
    rope.move(direction, steps)


# print(f"Puzzle 1: {len(rope.tail_visited)}")


class Movements(tuple, Enum):
    UP = (0, 1)
    UP_RIGHT = (1, 1)
    RIGHT = (1, 0)
    DOWN_RIGHT = (1, -1)
    DOWN = (0, -1)
    DOWN_LEFT = (-1, -1)
    LEFT = (-1, 0)
    UP_LEFT = (-1, 1)


head = Point(0, 0)
knots = [Point(0, 0) for _ in range(9)]
tail_visited: set[tuple[int]] = set()


def draw(level: list[list[str]]):
    logging.info("")
    for row in level[::-1]:
        logging.info("".join(row))


# size = 27
# oY = 6
# oX = 12
# level = [["." for _ in range(size)] for _ in range(size)]
# level[head.y + oY][head.x + oX] = "H"

# logging.info("\n== Initial State ==")


# draw(level)
for n_step, (direction, steps) in enumerate(commands):
    # logging.info(f"\n== {direction} {steps} ==")
    for step in range(steps):
        # level = [["." for _ in range(size)] for _ in range(size - 6)]
        head.move_direction(direction)
        for i, (knot_a, knot_b) in enumerate(
            zip([head, *knots][:-1], [head, *knots][1:])
        ):
            distance = get_distance(knot_a, knot_b)
            if distance > 1:
                # if are_diagonal(knot_a, knot_b):
                dx, dy = chebyshev_components(knot_a, knot_b)
                knot_b.x += int(dx / (abs(dx) or 1))
                knot_b.y += int(dy / (abs(dy) or 1))
                # else:
                # knot_b.move_direction(direction)
            # print(f"Knot {i + 1} d={distance}")

            if i == len(knots) - 1:
                tail_visited.add((knot_b.x, knot_b.y))

        # for k, knot in enumerate(knots):
        #     if level[knot.y + oY][knot.x + oX] in digits:
        #         continue
        #     level[knot.y + oY][knot.x + oX] = str(k + 1)
        # level[head.y + oY][head.x + oX] = "H"

        # draw(level)


pprint(len(tail_visited))
