from queue import Queue
from string import ascii_lowercase

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


def parse_elevation(elevation: str) -> int:
    if elevation == "S":
        elevation = "a"
    elif elevation == "E":
        elevation = "z"
    return ascii_lowercase.index(elevation)


class Node:
    def __init__(self, elevation: str, nodes=None) -> None:
        self.elevation = parse_elevation(elevation)
        self.is_start = elevation == "S"
        self.is_target = elevation == "E"
        self.neighbors: set[Node] = nodes or set()
        self.visited = False
        self.distance: int | None = None

    def __repr__(self) -> str:
        return f"<Node elevation={self.elevation} distance={self.distance}>"


def build_graph(lines: list[str]) -> list[Node]:
    nodes: list[list[Node]] = []

    for y, row in enumerate(lines):
        row_nodes = []
        for x, elevation in enumerate(row):
            node = Node(elevation=elevation)
            row_nodes.append(node)
        nodes.append(row_nodes)

    for y, row in enumerate(nodes):
        for x, node in enumerate(row):
            if x > 0:
                neighbor = nodes[y][x - 1]
                if neighbor.elevation <= node.elevation + 1:
                    node.neighbors.add(neighbor)
            if x < len(row) - 1:
                neighbor = nodes[y][x + 1]
                if neighbor.elevation <= node.elevation + 1:
                    node.neighbors.add(neighbor)
            if y > 0:
                neighbor = nodes[y - 1][x]
                if neighbor.elevation <= node.elevation + 1:
                    node.neighbors.add(neighbor)
            if y < len(nodes) - 1:
                neighbor = nodes[y + 1][x]
                if neighbor.elevation <= node.elevation + 1:
                    node.neighbors.add(neighbor)

    return [node for row in nodes for node in row]


def breadth_first_search(start_node: Node) -> None:
    queue: Queue[Node] = Queue()
    start_node.distance = 0
    queue.put(start_node)

    while not queue.empty():
        current_node = queue.get()
        for neighbor_node in current_node.neighbors:
            if neighbor_node.distance:
                continue
            neighbor_node.distance = current_node.distance + 1
            queue.put(neighbor_node)


nodes = build_graph(lines)

start_node = next(filter(lambda n: n.is_start, nodes))
breadth_first_search(start_node)
target_node = next(filter(lambda n: n.is_target, nodes))
print(f"Puzzle 1: {target_node.distance}")

distances = []
for start_node in filter(lambda n: n.elevation == 0, nodes):
    # reset distance calculation
    for node in nodes:
        node.distance = None

    breadth_first_search(start_node)
    target_node = next(filter(lambda n: n.is_target, nodes))
    if target_node.distance:  # no path
        distances.append(target_node.distance)

print(f"Puzzle 2: {min(distances)}")
