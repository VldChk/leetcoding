"""
LeetCode 222 - Count Complete Tree Nodes (Easy/Medium)
https://leetcode.com/problems/count-complete-tree-nodes/

Given the root of a complete binary tree, return the number of the nodes in the tree.

According to Wikipedia, every level, except possibly the last, is completely filled in a complete binary tree, and all nodes in the last level are as far left as possible. It can have between 1 and 2h nodes inclusive at the last level h.

Design an algorithm that runs in less than O(n) time complexity.

Solution idea:
  Walk down the leftmost spine to learn the tree height (left_depth).
  A perfect tree of that height has max_capacity = 2^left_depth - 1 nodes.
  Then walk the rightmost spine: if right_depth equals left_depth the
  tree is perfect (return max_capacity). Otherwise the missing nodes are
  in the rightmost subtree; walk back up subtracting two per absent
  rightmost leaf, identifying which last-level leaf positions are
  populated by maintaining a `seen_leafs` set and DFS-ing among unseen
  branches. Better than O(n) thanks to the spine probes; the leaf-level
  fixup stays bounded by the height.
"""

# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countNodes(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        left_depth = 1

        node = root

        while node.left is not None:
            node = node.left
            left_depth += 1

        if left_depth == 1:
            return 1
        elif left_depth == 2 and root.right is None:
            return 2

        max_capacity = 2**left_depth - 1

        right_depth = 1

        node = root
        stack = [node.left, node]

        while node.right is not None:
            node = node.right
            stack.append(node)
            right_depth += 1

        if left_depth == right_depth:
            return max_capacity
        else:
            seen_leafs = {node}
            node = stack.pop()
            depth = right_depth

        while stack:
            if depth == right_depth:
                if node.right is None and node.left is None:
                    seen_leafs.add(node)
                    depth -= 1
                    max_capacity -= 2
                    node = stack.pop()
                else:
                    return max_capacity if node.right is not None else max_capacity - 1
            else:
                if node.left in seen_leafs and node.right in seen_leafs:
                    depth -= 1
                    seen_leafs.add(node)
                    node = stack.pop()
                elif node.right not in seen_leafs:
                    stack.append(node)
                    depth += 1
                    node = node.right
                else:
                    stack.append(node)
                    depth += 1
                    node = node.left

        return max_capacity

        # if algo_depth == right_depth and is node.right -> exit
        # if algo_depth == right_depth and no node.right -> decrement max_capacity by 1, pull from stack
        #


if __name__ == "__main__":
    def build_tree(values):
        # LeetCode-style level-order list (None marks missing children).
        if not values:
            return None
        root = TreeNode(values[0])
        queue = [root]
        i = 1
        while queue and i < len(values):
            node = queue.pop(0)
            if i < len(values) and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
            if i < len(values) and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
        return root

    s = Solution()

    assert s.countNodes(build_tree([1, 2, 3, 4, 5, 6])) == 6      # Example 1
    assert s.countNodes(build_tree([])) == 0                      # Example 2
    assert s.countNodes(build_tree([1])) == 1                     # Example 3

    print("count_complete_tree_nodes.py: all tests passed")
