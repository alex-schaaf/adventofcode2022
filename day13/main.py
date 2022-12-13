import ast

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


def parse(lines: list[str]) -> list:
    return [ast.literal_eval(line) for line in lines if line]


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
    right order -> True
    wrong order -> False
    continue    -> None
    """
    for left, right in zip(list_a, list_b):
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


pairs = [(lists[i], lists[i + 1]) for i in range(0, len(lists), 2)]
indices = []
for i, (list_a, list_b) in enumerate(pairs):
    if compare_lists(list_a, list_b):
        indices.append(i + 1)


print(f"Puzzle 1: {sum(indices)}")

divider_packets = [[[2]], [[6]]]
lists += divider_packets

modified = [True]
while any(modified):
    modified = []
    for i in range(len(lists) - 1):
        if compare_lists(lists[i], lists[i + 1]):
            modified.append(False)
        else:
            lists[i], lists[i + 1] = lists[i + 1], lists[i]
            modified.append(True)


print(
    f"Puzzle 2: {(lists.index(divider_packets[0]) + 1) * (lists.index(divider_packets[1]) + 1)}"
)
