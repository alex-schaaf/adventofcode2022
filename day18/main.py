from collections import namedtuple
from pprint import pprint
from queue import Queue
import numpy as np

filepath = "./test"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


Cube = namedtuple("Cube", "x y z")
Extent = namedtuple("Extent", "x X y Y z Z")

DIRECTIONS = [
    (-1, 0, 0),
    (0, -1, 0),
    (0, 0, -1),
    (0, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
]


def parse(lines: list[str]) -> frozenset[Cube]:
    cubes: set[Cube] = set()
    for line in lines:
        x, y, z = (int(c) for c in line.split(","))
        cubes.add(Cube(x + 1, y + 1, z + 1))
    return frozenset(cubes)


def get_extent(cubes: frozenset[Cube]) -> Extent:
    xs = [c.x for c in cubes]
    ys = [c.y for c in cubes]
    zs = [c.z for c in cubes]
    minx, maxx = min(xs), max(xs) + 2
    miny, maxy = min(ys), max(ys) + 2
    minz, maxz = min(zs), max(zs) + 2
    return Extent(minx, maxx, miny, maxy, minz, maxz)


def in_bounds(grid, point) -> bool:
    x, y, z = point
    if (
        0 <= x
        and x < grid.shape[0]
        and 0 <= y
        and y < grid.shape[1]
        and 0 <= z
        and z < grid.shape[2]
    ):
        return True
    return False


def fill(grid: np.ndarray, start: tuple[int, int, int]):
    queue = Queue()
    queue.put(start)

    while not queue.empty():
        point = queue.get()
        value = grid[*point]
        if value != 0:
            continue

        grid[*point] = 2
        for dx, dy, dz in DIRECTIONS:
            x, y, z = point[0] + dx, point[1] + dy, point[2] + dz
            if in_bounds(grid, (x, y, z)):
                queue.put((x, y, z))

    return grid


def get_surface_area(cubes: frozenset[Cube]) -> int:
    surface = 0
    for cube in cubes:
        for dx, dy, dz in DIRECTIONS:
            dc = Cube(cube.x + dx, cube.y + dy, cube.z + dz)
            if dc in cubes:
                continue
            else:
                surface += 1
    return surface


def get_outer_surface_area(cubes: frozenset[Cube], grid: np.ndarray) -> int:
    surface = 0

    for cube in cubes:
        for dx, dy, dz in DIRECTIONS:
            p = cube.x + dx, cube.y + dy, cube.z + dz
            if in_bounds(grid, p) and grid[*p] == 2:
                surface += 1

    return surface


if __name__ == "__main__":
    cubes = parse(lines)
    surface_area = get_surface_area(cubes)
    print(f"Puzzle 1: {surface_area}")

    extent = get_extent(cubes)
    grid = np.zeros((extent.X, extent.Y, extent.Z), dtype=int)
    for cube in cubes:
        grid[*cube] = 1

    pprint(grid)
    grid = fill(grid, (0, 0, 0))

    outer_surface_area = get_outer_surface_area(cubes, grid)
    print(outer_surface_area)
