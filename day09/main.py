from pprint import pprint
from dataclasses import dataclass
from enum import Enum


filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


commands: list[tuple[str, int]] = []
for line in lines:
    direction, steps = line.split()
    commands.append((direction, int(steps)))

pprint(commands)


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


class Rope:
    def __init__(self, x: int, y: int) -> None:
        self.head = Point(x=x, y=y)
        self.tail = Point(x=x, y=y)
        self.tail_visited = set((x, y))

    def chebyshev_components(self) -> tuple[int]:
        return (self.head.x - self.tail.x, self.head.y - self.tail.y)

    def distance(self) -> int:
        """Chebyshev distance between head and tail"""
        dx, dy = self.chebyshev_components()
        return max((abs(dx), abs(dy)))

    def diagonal(self) -> bool:
        """Check if head and tail are in diagonal arrangement"""
        dx, dy = self.chebyshev_components()
        return all((abs(dx), abs(dy)))

    def move(self, direction: Direction, steps: int) -> None:
        for _ in range(steps):
            self.head.move_direction(direction)
            if self.distance() > 1:
                if self.diagonal():
                    dx, dy = self.chebyshev_components()
                    self.tail.x += int(dx / abs(dx))
                    self.tail.y += int(dy / abs(dy))
                else:
                    self.tail.move_direction(direction)
                self.tail_visited.add((self.tail.x, self.tail.y))


rope = Rope(0, 0)

for (direction, steps) in commands:
    rope.move(direction, steps)

print("head", rope.head)
print("tail", rope.tail)
pprint(len(rope.tail_visited))
