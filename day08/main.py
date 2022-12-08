filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]

tree_heights: list[list[int]] = []
is_visible: list[list[bool]] = []
scenic_scores: list[list[int]] = []

for line in lines:
    tree_heights.append([int(c) for c in line])
    is_visible.append([0 for _ in range(len(line))])
    scenic_scores.append([0 for _ in range(len(line))])


for y, row in enumerate(tree_heights):
    for x, height in enumerate(row):
        if y == 0 or y == len(tree_heights) - 1 or x == 0 or x == len(row) - 1:
            is_visible[y][x] = 1


def check_tree_heights(height: int, tree_heights: list[int]) -> bool:
    for tree_height in tree_heights:
        if height <= tree_height:
            return False
    return True


for y, row in enumerate(tree_heights):
    if y == 0 or y == len(tree_heights) - 1:
        continue

    # # from left
    for x, height in enumerate(row):
        if check_tree_heights(height, row[:x]):
            is_visible[y][x] = 1

    # # from right
    for x, height in enumerate(row):
        if check_tree_heights(height, row[x + 1 :]):
            is_visible[y][x] = 1

for x in range(len(tree_heights[0])):
    if x == 0 or x == len(tree_heights) - 1:
        continue

    column = [row[x] for row in tree_heights]

    # from top
    for y, height in enumerate(column):
        if check_tree_heights(height, column[:y]):
            is_visible[y][x] = 1

    # from bottom
    for y, height in enumerate(column):
        if check_tree_heights(height, column[y + 1 :]):
            is_visible[y][x] = 1


print(f"Puzzle 1: {sum([sum(r) for r in is_visible])}")


def get_viewing_distance(height: int, tree_heights: list[int]) -> int:
    viewing_distance = 0
    for tree_height in tree_heights:
        viewing_distance += 1
        if height <= tree_height:
            break
    return viewing_distance


def get_scenic_score(x: int, y: int, tree_heights: list[list[int]]) -> int:
    height = tree_heights[y][x]

    viewing_distance_right = get_viewing_distance(height, tree_heights[y][x + 1 :])
    viewing_distance_left = get_viewing_distance(height, tree_heights[y][:x][::-1])

    column = [row[x] for row in tree_heights]

    viewing_distance_up = get_viewing_distance(height, column[:y][::-1])
    viewing_distance_down = get_viewing_distance(height, column[y + 1 :])

    return (
        viewing_distance_right
        * viewing_distance_left
        * viewing_distance_up
        * viewing_distance_down
    )


for y, row in enumerate(tree_heights):
    for x, height in enumerate(row):
        scenic_score = get_scenic_score(x, y, tree_heights)
        scenic_scores[y][x] = scenic_score


print(f"Puzzle 2: {max([max(r) for r in scenic_scores])}")
