"""
LeetCode 111 - Minimum Depth of Binary Tree (Easy)
https://leetcode.com/problems/minimum-depth-of-binary-tree/

Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.

Solution idea:
  BFS level-by-level. The inner `_bfs` helper drains the current layer
  out of `queue` (used as a stack via .pop()), accumulates next-layer
  children in `layer`, and short-circuits the moment any node turns out
  to be a leaf — that's the closest leaf, so it clears the queue and
  returns. The outer driver bumps `min_path` once per layer until the
  short-circuit fires (or the tree is exhausted), at which point
  min_path equals the minimum depth.
"""

# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# from collections import deque
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        def _bfs(queue):
            layer = []
            while queue:
                node = queue.pop()
                # print(f"{node}: {node.left is None}; {node.right is None}")
                if node.left is None and node.right is None:
                    while queue:
                        queue.pop()
                    return
                elif node:
                    if node.left:
                        layer.append(node.left)
                    if node.right:
                        layer.append(node.right)
            queue.extend(layer)
            return

        if not root:
            return 0

        min_path = 0
        queue = [root]

        while queue:
            _bfs(queue)
            min_path += 1

        return min_path


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

    # Example 1: balanced tree, nearest leaf at depth 2.
    assert s.minDepth(build_tree([3, 9, 20, None, None, 15, 7])) == 2
    # Example 2: skinny right-only chain of 5.
    assert s.minDepth(build_tree([2, None, 3, None, 4, None, 5, None, 6])) == 5

    print("minimum_depth.py: all tests passed")
