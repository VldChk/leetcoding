#from day_11_input import real_input

test_input = [
    "aaa: you hhh",
    "you: bbb ccc",
    "bbb: ddd eee",
    "ccc: ddd eee fff",
    "ddd: ggg",
    "eee: out",
    "fff: out",
    "ggg: out",
    "hhh: ccc fff iii",
    "iii: out",
]

INPUT = test_input


class GraphNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child_node):
        if isinstance(child_node, GraphNode):
            self.children.append(child_node)
        elif isinstance(child_node, list):
            self.children.extend(child_node)
        else:
            raise ValueError("Child node must be a GraphNode or a list of GraphNodes")


def build_graph(input_lines):
    nodes = {}
    for line in input_lines:
        parent_name, children_str = line.split(": ")
        parent_node = nodes.setdefault(parent_name, GraphNode(parent_name))
        for child_name in children_str.split(" "):
            child_node = nodes.setdefault(child_name, GraphNode(child_name))
            parent_node.add_child(child_node)
    return nodes


def count_paths(nodes, start_name, target_name="out", must_visit=None):
    required = frozenset(must_visit or [])
    memo = {}
    active = set()

    def dfs(current_name, remaining_required):
        key = (current_name, remaining_required)
        if key in memo:
            return memo[key]
        if current_name in active:
            return 0
        
        active.add(current_name)
        next_required = remaining_required - {current_name}

        if current_name == target_name:
            result = 1 if not next_required else 0
        else:
            result = sum(dfs(child.name, next_required) for child in nodes[current_name].children)

        active.remove(current_name)
        memo[key] = result
        return result

    return dfs(start_name, required)


if __name__ == "__main__":
    nodes = build_graph(INPUT)
    total_paths = count_paths(nodes, "you")
    print(f"Total paths found: {total_paths}")

    nodes = build_graph(INPUT)
    total_paths_part_two = count_paths(nodes, "svr", must_visit={"dac", "fft"})
    print(f"Total paths found in part two: {total_paths_part_two}")
