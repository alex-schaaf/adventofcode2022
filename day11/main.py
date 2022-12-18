import logging
import math
import queue
from dataclasses import dataclass
from pprint import pprint
from typing import Callable

logging.basicConfig(level=logging.INFO, format="%(message)s")

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


@dataclass
class Monkey:
    items: queue.Queue
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    divisible_by: int
    inspections: int = 0


def get_operation(op: str) -> Callable[[int], int]:
    return lambda old: eval(op)


def get_test(divisible_by: int, on_true: int, on_false: int) -> Callable[[int], bool]:
    return (
        lambda worry_level: on_true if (worry_level % divisible_by == 0) else on_false
    )


def adjust_worry_level(worry_level: int) -> int:
    return math.floor(worry_level / 3)


def parse(lines: list[str], n: int = 7) -> list[Monkey]:
    monkeys = []

    for i in range(0, len(lines) + 1, n):
        starting_items = [
            int(item) for item in lines[i + 1].lstrip("  Starting items: ").split(",")
        ]
        starting_queue = queue.Queue()
        for item in starting_items:
            starting_queue.put(item)

        raw_operation = lines[i + 2].split(" = ")[1]
        # if raw_operation == "old * old":
        #     raw_operation = "old"
        # print(raw_operation)
        operation = get_operation(raw_operation)

        # test
        divisible_by = int(lines[i + 3].lstrip("  Test: divisible by "))
        on_true = int(lines[i + 4].lstrip("    If true: throw to monkey "))
        on_false = int(lines[i + 5].lstrip("    If false: throw to monkey "))

        test = get_test(divisible_by, on_true, on_false)

        monkey = Monkey(
            items=starting_queue,
            operation=operation,
            test=test,
            divisible_by=divisible_by,
        )
        monkeys.append(monkey)

    return monkeys


monkeys = parse(lines)


# the product of all divisors that need to resolve to remainder zero
# 23 * 19 = 437
# 23 % 437 = 23
# 19 % 437 = 19
# -> if B > A, then A mod B -> A
# given that the product of all divisors is bigger than all the starting item
# worry levels, the worry levels will just remain the same when % with the
# product, leaving the remainder always as it should be


COMMON_MOD = 1
for divisible_by in [m.divisible_by for m in monkeys]:
    COMMON_MOD *= divisible_by


def drastically_adjust_worry_level(worry_level: int) -> int:
    return worry_level % COMMON_MOD


for round in range(10_000):
    for _, monkey in enumerate(monkeys):
        # logging.debug(f"Monkey {m}")
        while not monkey.items.empty():
            item = monkey.items.get()
            monkey.inspections += 1
            # logging.debug(f" Monkey {m} inspects an item with a worry level of {item}")
            worry_level = monkey.operation(item)
            # logging.debug(f"  Worry level is raised to {worry_level}")
            # logging.debug(f"  Worry level is divided by 3 to {worry_level}")
            target = monkey.test(worry_level)

            # worry_level = adjust_worry_level(worry_level)
            worry_level = drastically_adjust_worry_level(worry_level)
            # logging.debug(f"  Throw item to monkey {target}")
            monkeys[target].items.put(worry_level)

        # monkey.items = queue.Queue([i % factor for i in monkey.items.queue])

# logging.info(f"After round {round + 1}")
# for m, monkey in enumerate(monkeys):
#     # logging.info(f" Monkey {m}: {list(monkey.items.queue)}")
#     logging.info(f" Monkey {m}: {monkey.inspections}")


monkeys = sorted(monkeys, key=lambda m: m.inspections, reverse=True)

print(f"Result: {monkeys[0].inspections * monkeys[1].inspections}")
