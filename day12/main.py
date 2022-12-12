from queue import Queue
from string import ascii_lowercase

filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


class Node:
    def __init__(self, elevation: str) -> None:
        self.elevation = self.parse_elevation(elevation)
        self.is_start = elevation == "S"
        self.is_target = elevation == "E"
        self.neighbors: set[Node] = set()
        self.distance: int | None = None

    def __repr__(self) -> str:
        return f"<Node elevation={self.elevation} distance={self.distance}>"

    @staticmethod
    def parse_elevation(elevation: str) -> int:
        """Converts ascii lowercase elevation encoding into integer elevation (a=0, z=25)"""
        if elevation == "S":
            elevation = "a"
        elif elevation == "E":
            elevation = "z"
        return ascii_lowercase.index(elevation)


def build_graph(lines: list[str]) -> set[Node]:
    """
    Build up graph based on the puzzle input lines and elevation-based
    connectivity rules.
    """
    nodes = [[Node(elevation) for elevation in row] for row in lines]

    def maybe_add_neighbor(node: Node, neighbor: Node):
        if neighbor.elevation <= node.elevation + 1:
            node.neighbors.add(neighbor)

    # add edges to every node
    for y, row in enumerate(nodes):
        for x, node in enumerate(row):
            if x > 0:
                maybe_add_neighbor(node, nodes[y][x - 1])
            if x < len(row) - 1:
                maybe_add_neighbor(node, nodes[y][x + 1])
            if y > 0:
                maybe_add_neighbor(node, nodes[y - 1][x])
            if y < len(nodes) - 1:
                maybe_add_neighbor(node, nodes[y + 1][x])

    return {node for row in nodes for node in row}


def breadth_first_search(start_node: Node) -> None:
    """
    Performs breadth first search from a given start Node by setting
    the distance property on every Node to the distance travelled to
    get there.
    """
    queue: Queue[Node] = Queue()

    start_node.distance = 0
    queue.put(start_node)

    while not queue.empty():
        current_node = queue.get()

        for neighbor in current_node.neighbors:
            if neighbor.distance:
                continue

            neighbor.distance = current_node.distance + 1
            queue.put(neighbor)


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
