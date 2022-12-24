from collections import namedtuple

filepath = "./input.txt"

Location = namedtuple("Location", "x y")


MOVE_DIRECTIONS: list[tuple[tuple[Location, Location, Location], Location]] = [
    (  # N, NE, or NW
        (Location(-1, -1), Location(0, -1), Location(1, -1)),
        Location(0, -1),
    ),
    (  # S, SE, or SW
        (Location(-1, 1), Location(0, 1), Location(1, 1)),
        Location(0, 1),
    ),
    (  # W, NW, or SW
        (Location(-1, -1), Location(-1, 0), Location(-1, 1)),
        Location(-1, 0),
    ),
    (  # E, NE, or SE
        (Location(1, -1), Location(1, 0), Location(1, 1)),
        Location(1, 0),
    ),
]

NEIGHBOR_DIRECTIONS = [(x, y) for x in range(-1, 2) for y in range(-1, 2)]
NEIGHBOR_DIRECTIONS.remove((0, 0))


def parse(lines: list[str]) -> set[Location]:
    elves = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                elves.add(Location(x, y))
    return elves


def _get_proposal(
    loc: Location,
    locations: Location,
) -> Location | None:
    neighbors = []
    for (dx, dy) in NEIGHBOR_DIRECTIONS:
        if Location(loc.x + dx, loc.y + dy) in locations:
            neighbors.append(True)
        else:
            neighbors.append(False)
    if not any(neighbors):
        return None

    targets = []
    for directions, t in MOVE_DIRECTIONS:
        for dloc in directions:
            proposal = Location(loc.x + dloc.x, loc.y + dloc.y)
            if proposal in locations:
                break
        else:
            targets.append(Location(loc.x + t.x, loc.y + t.y))

    match len(targets):
        case 0:  # everything is full - don't move!
            return None
        case 4:  # everything is empty - don't move!
            return None
        case _:  # get the first valid target
            return targets[0]


def propose(locations: set[Location]) -> dict[Location, Location]:
    """Get proposals for new locations for all given locations."""
    proposals = dict()
    for loc in locations:
        if proposal := _get_proposal(loc, locations):
            proposals[loc] = proposal
    return proposals


def paint(locations: set[Location], nx: int, ny: int) -> None:
    print("     " + "".join([f"{x:02d}"[0] for x in range(nx)]))
    print("     " + "".join([f"{x:02d}"[1] for x in range(nx)]))
    print("    -" + "".join(["-" for _ in range(nx)]))
    for y in range(ny):
        print(f"{y:02d} | ", end="")
        for x in range(nx):
            loc = Location(x, y)
            if loc in locations:
                print("#", end="")
            else:
                print(".", end="")
        print("")


def move(
    locations: set[Location],
    proposals: dict[Location, Location],
) -> set[Location]:
    """Move all elves to their proposed positions.

    If more than one elf wants to move to a position, none of them move.
    """
    new_locations = set()
    for current_loc in locations:
        proposal_loc = proposals.get(current_loc)
        if not proposal_loc:
            # no valid proposal was available, stay in place!
            new_locations.add(current_loc)
        elif list(proposals.values()).count(proposal_loc) > 1:
            # more than one elve want to move here, stay in place!
            new_locations.add(current_loc)
        else:
            # a valid location exists, move!
            new_locations.add(proposal_loc)
    return new_locations


if __name__ == "__main__":
    with open(filepath, "r") as file:
        lines = [line.strip("\n") for line in file.readlines()]
    locations = parse(lines)

    round = 0
    while True:
        proposals = propose(locations)
        newLocations = move(locations, proposals)

        if locations == newLocations:
            print(f"Puzzle 2: {round+1}")
            break

        locations = newLocations
        MOVE_DIRECTIONS = MOVE_DIRECTIONS[1:] + [MOVE_DIRECTIONS[0]]

        if round == 9:
            xs = [loc.x for loc in locations]
            ys = [loc.y for loc in locations]

            count = 0
            for y in range(min(ys), max(ys) + 1):
                for x in range(min(xs), max(xs) + 1):
                    if Location(x, y) in locations:
                        continue
                    else:
                        count += 1

            print(f"Puzzle 1: {count}")

        round += 1
