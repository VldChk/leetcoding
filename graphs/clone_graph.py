"""
LeetCode 133 - Clone Graph (Medium)
https://leetcode.com/problems/clone-graph/

Given a reference of a node in a connected undirected graph.

Return a deep copy (clone) of the graph.

Each node in the graph contains a value (int) and a list of its
neighbors (List[Node]).

class Node {
    public int val;
    public List<Node> neighbors;
}

Solution idea:
  Recursive DFS with a memo dict mapping original node -> cloned node.
  When we first encounter a node, create its clone, register it in
  the memo *before* recursing on neighbors (so cycles don't loop
  forever), then recursively clone each neighbor and attach. Subsequent
  visits return the already-built clone from the memo.
"""
from __future__ import annotations
from typing import Optional

class Node:
    def __init__(self, val: int = 0, neighbors: Optional[list['Node']] = None):
        self.val = val
        self.neighbors: list['Node'] = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        def _dfs(node: Optional['Node']) -> Optional['Node']:
            if not node:
                return node
            if node in memory:
                return memory[node]
            new_node = Node(node.val, [])
            memory[node] = new_node
            if not node.neighbors:
                return new_node
            n_neighbors: list[Optional['Node']] = [_dfs(el) for el in node.neighbors]
            new_node.neighbors = n_neighbors
            return new_node

        memory: dict['Node', 'Node'] = {}

        return _dfs(node)


if __name__ == "__main__":
    def build(adj_list):
        """LeetCode-style adjacency list (1-indexed); empty list -> None."""
        if not adj_list:
            return None
        nodes = [Node(i + 1, []) for i in range(len(adj_list))]
        for i, neighbors in enumerate(adj_list):
            nodes[i].neighbors = [nodes[j - 1] for j in neighbors]
        return nodes[0]

    def to_adj(root):
        if root is None:
            return []
        # BFS to enumerate nodes in val order.
        seen, order = {root.val: root}, [root]
        i = 0
        while i < len(order):
            for nb in order[i].neighbors:
                if nb.val not in seen:
                    seen[nb.val] = nb
                    order.append(nb)
            i += 1
        by_val = sorted(seen.values(), key=lambda n: n.val)
        return [[nb.val for nb in n.neighbors] for n in by_val]

    s = Solution()

    # Example 1
    adj1 = [[2, 4], [1, 3], [2, 4], [1, 3]]
    cloned1 = s.cloneGraph(build(adj1))
    assert to_adj(cloned1) == adj1
    assert cloned1 is not build(adj1)            # actually a copy

    # Example 2: single node, no neighbors
    cloned2 = s.cloneGraph(build([[]]))
    assert to_adj(cloned2) == [[]]

    # Example 3: empty graph
    assert s.cloneGraph(build([])) is None

    print("clone_graph.py: all tests passed")
