from pprint import pprint
import ast

filepath = "./test"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


def parse(lines: list[str]):
    lists = []
    for line in lines:
        if line == "":
            continue
        lists.append(ast.literal_eval(line))
    return lists


lists = parse(lines)


def compare_ints(left: int, right: int) -> bool | None:
    if left < right:
        return True
    elif left == right:
        return None
    else:  # left > right
        return False


def compare_lists(list_a: list, list_b: list) -> bool | None:
    """
    True -> right order
    False -> wrong order
    None -> continue
    """
    for left, right in zip(list_a, list_b):
        # print(f"  - Compare {left} vs {right}")
        if isinstance(left, int) and isinstance(right, int):
            result = compare_ints(left, right)
            if result is not None:
                return result
        elif isinstance(left, list) and isinstance(right, list):
            result = compare_lists(left, right)
            if result is not None:
                return result
        else:
            if isinstance(left, int):
                left = [left]
            else:
                right = [right]
            result = compare_lists(left, right)
            if result is not None:
                return result

    if len(list_a) < len(list_b):
        return True
    elif len(list_a) == len(list_b):
        return None
    else:
        return False


indices = []

pairs = []
for p in range(0, len(lists), 2):
    pairs.append((lists[p], lists[p + 1]))


for i, (list_a, list_b) in enumerate(pairs):
    result = compare_lists(list_a, list_b)
    if result is True:
        indices.append(i + 1)


print(f"Puzzle 1: {sum(indices)}")
