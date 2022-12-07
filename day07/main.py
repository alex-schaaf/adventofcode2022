filepath = "./input"

with open(filepath, "r") as file:
    lines = [line.strip("\n") for line in file.readlines()]


class Node:
    def __init__(self, name: str, parent=None, children=None, files=None) -> None:
        self.name = name
        self.parent = parent
        self.children: list[Node] = children or []
        self.files: dict[str, int] = files or {}

    def __repr__(self) -> str:
        return f"<Node name='{self.name}' size={self.get_total_size()}>"

    def get_total_size(self) -> int:
        size = sum([size for size in self.files.values()])
        size += sum([c.get_total_size() for c in self.children])
        return size


root_node: Node | None = None
current_node: Node | None = None

for line in lines:
    if line.startswith("$ cd"):
        _, _, folder_name = line.split()
        if folder_name == "..":
            current_node = current_node.parent
        else:
            if not current_node:
                current_node = Node(folder_name)
                root_node = current_node
            else:
                new_node = Node(folder_name, parent=current_node)
                new_node.parent.children.append(new_node)
                current_node = new_node
    elif line.startswith("$ ls"):
        continue
    elif line.startswith("dir"):
        continue
    else:
        size, filename = line.split()
        current_node.files[filename] = int(size)


def find_leaves(root: Node) -> set[Node]:
    queue: list[Node] = [*root.children]
    leaves = set()

    while queue:
        current_node = queue.pop()
        if not current_node.children:
            leaves.add(current_node)
        else:
            queue = queue + [*current_node.children]

    return leaves


def get_all_nodes(root: Node) -> set[Node]:
    nodes = set([root])
    queue = [*root.children]

    while queue:
        current_node = queue.pop()
        queue += [*current_node.children]
        nodes.add(current_node)

    return nodes


nodes = get_all_nodes(root_node)

print(
    f"Puzzle 1: {sum([n.get_total_size() for n in nodes if n.get_total_size() <= 100000])}"
)


total_disk_space = 70000000
required_unused_disk_space = 30000000
used_disk_space = root_node.get_total_size()
remaining_disk_space = total_disk_space - used_disk_space
disk_space_to_free_up = required_unused_disk_space - remaining_disk_space

nodes_sorted = sorted(nodes, key=lambda n: n.get_total_size(), reverse=False)

for node in nodes_sorted:
    if node.get_total_size() >= disk_space_to_free_up:
        print(f"Puzzle 2: {node.get_total_size()}")
        break
