"""
Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node reference (possibly updated) of the BST.

Basically, the deletion can be divided into two stages:

Search for a node to remove.
If the node is found, delete the node.
"""


# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        def _delete(node):
            if not node.right:
                return node.left
            elif not node.left:
                return node.right
            elif not node.right.left:
                node.right.left = node.left
                return node.right
            elif not node.left.right:
                node.left.right = node.right
                return node.left
            else:
                parent = node
                next_node = node.right
                while next_node.left:
                    parent = next_node
                    next_node = next_node.left
                node.val = next_node.val
                parent.left = next_node.right
                return node

        if not root:
            return
        elif root.val == key:
            return _delete(root)
        parent = root
        direction = None
        node = root

        while node:
            if node.val == key:
                if direction == "left":
                    parent.left = _delete(node)
                else:
                    parent.right = _delete(node)
                return root
            else:
                if node.val > key:
                    if node.left:
                        direction = "left"
                        parent = node
                        node = node.left
                    else:
                        return root
                else:
                    if node.right:
                        direction = "right"
                        parent = node
                        node = node.right
                    else:
                        return root
