from collections import namedtuple, defaultdict
from enum import Enum
from pprint import pprint


class Tile(str, Enum):
    WALL = "#"
    GROUND = "."
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"
    EXPEDITION = "E"


BLIZZARD_TILES = {Tile.UP, Tile.DOWN, Tile.LEFT, Tile.RIGHT}


class Movement(tuple, Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


Location = namedtuple("Location", "x y")


def parse(
    lines: list[str],
) -> tuple[defaultdict[Location, list[Tile]], Location, Location, set[Location]]:
    blizzards: defaultdict[Location, list[Tile]] = defaultdict(list)
    walls: set[Location] = set()
    start = None
    end = None
    for y, line in enumerate(lines):
        for x, tile in enumerate(line):
            if y == 0 and tile == Tile.GROUND:
                start = Location(x, y)
            elif y == len(lines) - 1 and tile == Tile.GROUND:
                end = Location(x, y)
            elif tile in BLIZZARD_TILES:
                for t in BLIZZARD_TILES:
                    if t == tile:
                        blizzards[Location(x, y)].append(t)
            elif tile == Tile.WALL:
                walls.add(Location(x, y))
    return blizzards, start, end, walls


def paint(
    blizzards: defaultdict[Location, list[Tile]],
    start: Location,
    end: Location,
    expedition: Location,
    nX: int,
    nY: int,
) -> None:
    print("    " + "".join([f"{i}" for i in range(nX)]))
    print("    " + "".join(["-" for _ in range(nX)]))
    for y in range(nY):
        print(f"{y} | ", end="")
        for x in range(nX):
            loc = Location(x, y)
            if loc == expedition:
                print(Tile.EXPEDITION.value, end="")
            elif loc == start or loc == end:
                print(Tile.GROUND.value, end="")
            elif y == 0 or y == nY - 1 or x == 0 or x == nX - 1:
                print(Tile.WALL.value, end="")
            elif loc in blizzards:
                if len(blizzards[loc]) > 1:
                    print(len(blizzards[loc]), end="")
                else:
                    print(blizzards[loc][0].value, end="")
            else:
                print(Tile.GROUND.value, end="")
        print("")


def get_new_blizzard_loc(
    loc: Location,
    direction: Tile,
    nX: int,
    nY: int,
) -> Location:
    match direction:
        case Tile.UP:
            dx, dy = Movement.UP.value
        case Tile.RIGHT:
            dx, dy = Movement.RIGHT.value
        case Tile.DOWN:
            dx, dy = Movement.DOWN.value
        case Tile.LEFT:
            dx, dy = Movement.LEFT.value
        case _:
            raise ValueError("Invalid direction")

    new_location = Location(loc.x + dx, loc.y + dy)

    if new_location.x == 0:
        new_location = Location(nX - 2, new_location.y)
    if new_location.y == 0:
        new_location = Location(new_location.x, nY - 2)
    if new_location.x == nX - 1:
        new_location = Location(1, new_location.y)
    if new_location.y == nY - 1:
        new_location = Location(new_location.x, 1)

    return new_location


def simulate(
    blizzards: defaultdict[Location, list[Tile]], nX: int, nY: int
) -> defaultdict[Location, list[Tile]]:
    new_blizzards = defaultdict(list)
    for location, blizzards_at_loc in blizzards.items():
        for b in blizzards_at_loc:
            new = get_new_blizzard_loc(location, b, nX, nY)
            new_blizzards[new].append(b)
    return new_blizzards


if __name__ == "__main__":
    filepath = "./test2.txt"
    with open(filepath, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]

    nY = len(lines)
    nX = len(lines[0])
    blizzards, start, end, walls = parse(lines)
    # pprint(blizzards)

    expedition = Location(start.x, start.y)

    paint(blizzards, start, end, expedition, nX, nY)

    for minute in range(2):
        print(f"\n== Minute {minute + 1} ==\n")
        blizzards = simulate(blizzards, nX, nY)

        paint(blizzards, start, end, expedition, nX, nY)
