"""
Given a binary tree, find its minimum depth.

The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.

Note: A leaf is a node with no children.
Example:"""

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
