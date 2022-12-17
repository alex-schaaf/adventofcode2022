from collections import defaultdict
from dataclasses import dataclass

filepath = "./test"

with open(filepath, "r") as file:
    jet_pattern = file.read()


CHAMBER_WIDTH = 7

shapes = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]


@dataclass
class Rock:
    x: int
    y: int
    shape_idx: int

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy


def create_rock(n_fallen_rocks: int, highest_y: int) -> Rock:
    return Rock(2, highest_y + 4, n_fallen_rocks % len(shapes))


def can_move(
    rock: Rock, d: tuple[int, int], world: dict[tuple[int, int], bool]
) -> bool:
    shape = shapes[rock.shape_idx]
    for (x, y) in shape:
        new_x = rock.x + x + d[0]
        new_y = rock.y + y + d[1]
        if new_y < 0 or new_x < 0 or new_x >= CHAMBER_WIDTH:
            return False
        if world[(new_x, new_y)]:
            return False
    return True


def paint(world: dict[tuple[int, int], bool], rock: Rock | None = None) -> None:
    for y in reversed(range(0, 25)):
        print(f"{y:02d} |", end="")
        for x in range(CHAMBER_WIDTH):
            if rock:
                shape = shapes[rock.shape_idx]
                if (x - rock.x, y - rock.y) in shape:
                    print("@", end="")
                else:
                    if world[(x, y)]:
                        print("#", end="")
                    else:
                        print(".", end="")
            else:
                if world[(x, y)]:
                    print("#", end="")
                else:
                    print(".", end="")
        print("|")
    print("   +-------+")


world: dict[tuple[int, int], bool] = defaultdict(bool)
jet_index = 0
current_rock = None
n_fallen_rocks = 0
highest_y = -1
while n_fallen_rocks < 2022:
    current_rock = create_rock(n_fallen_rocks, highest_y)

    falling = True
    i = 0
    while falling:
        if i % 2 == 0:
            jet_direction = jet_pattern[jet_index]
            d = (-1, 0) if jet_direction == "<" else (1, 0)
            if can_move(current_rock, d, world):
                current_rock.move(*d)
            jet_index = (jet_index + 1) % len(jet_pattern)
        else:
            d = (0, -1)
            if falling := can_move(current_rock, d, world):
                current_rock.move(*d)
        i += 1

    for (x, y) in shapes[current_rock.shape_idx]:
        nx = current_rock.x + x
        ny = current_rock.y + y
        world[(nx, ny)] = True
        if ny > highest_y:
            highest_y = ny

    n_fallen_rocks += 1

print(highest_y + 1)
