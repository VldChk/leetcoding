"""
LeetCode 138 - Copy List with Random Pointer (Medium)
https://leetcode.com/problems/copy-list-with-random-pointer/

A linked list of n nodes is given where every node also has a `random`
pointer that may point at any node of the list or at null. Build a deep
copy: exactly n brand new nodes with the same values, whose `next` and
`random` pointers reproduce the original structure using only the new
nodes — nothing in the copy may point back into the original list.

The list is written as [val, random_index] pairs, where random_index is
the index of the node the random pointer targets, or null:
  [[7,null],[13,0],[11,4],[10,2],[1,0]] -> [[7,null],[13,0],[11,4],[10,2],[1,0]]
  [[1,1],[2,1]]                         -> [[1,1],[2,1]]
  [[3,null],[3,0],[3,null]]             -> [[3,null],[3,0],[3,null]]

Solution idea:
  A hash map from each original node to its copy. First walk the list and
  collect the original nodes in order. Then create the copies back to
  front, so each copy's `next` already exists when it is built. A final
  pass wires every copy's `random` by looking up the original's random
  target in the map. O(n) time, O(n) space.
"""
from typing import Any, Optional


# Definition for a Node.
class Node:
    def __init__(self, x: int, next: Optional['Node'] = None, random: Optional['Node'] = None) -> None:
        self.val = x
        self.next = next
        self.random = random


class Solution:
    def copyRandomList(self, head: Optional[Node]) -> Optional[Node]:
        if not head:
            return None
        last_node = head
        orig_nodes = [last_node]
        while last_node.next:
            last_node = last_node.next
            orig_nodes.append(last_node)

        copies: dict[Node, Node] = {}
        new_node: Optional[Node] = None
        for node in reversed(orig_nodes):
            new_node = Node(node.val, new_node)
            copies[node] = new_node

        for node in orig_nodes:
            if node.random:
                copies[node].random = copies[node.random]

        return new_node


if __name__ == "__main__":
    def from_pairs(pairs: list[list[Any]]) -> Optional[Node]:
        nodes = [Node(val) for val, _ in pairs]
        for i, (_, rnd) in enumerate(pairs):
            nodes[i].next = nodes[i + 1] if i + 1 < len(nodes) else None
            nodes[i].random = nodes[rnd] if rnd is not None else None
        return nodes[0] if nodes else None

    def to_pairs(head: Optional[Node]) -> tuple[list[list[Any]], set[Node]]:
        nodes: list[Node] = []
        while head:
            nodes.append(head)
            head = head.next
        index = {node: i for i, node in enumerate(nodes)}
        return [[node.val, index[node.random] if node.random else None] for node in nodes], set(nodes)

    s = Solution()

    # Official examples: same structure, and not a single node shared with the original
    for pairs in ([[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
                  [[1, 1], [2, 1]],
                  [[3, None], [3, 0], [3, None]]):
        original = from_pairs(pairs)
        copied, copied_nodes = to_pairs(s.copyRandomList(original))
        _, original_nodes = to_pairs(original)
        assert copied == pairs
        assert not copied_nodes & original_nodes

    print("copy_list_with_random_pointer.py: all tests passed")
