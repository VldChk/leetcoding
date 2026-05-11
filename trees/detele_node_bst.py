"""
LeetCode 450 - Delete Node in a BST (Medium)
https://leetcode.com/problems/delete-node-in-a-bst/

(Filename "detele_node_bst" is a typo for "delete_node_bst".)

Given a root node reference of a BST and a key, delete the node with
the given key in the BST. Return the root node reference (possibly
updated) of the BST.

Basically, the deletion can be divided into two stages:

Search for a node to remove.
If the node is found, delete the node.

Solution idea:
  Walk down the BST while remembering the parent pointer and the
  direction taken. When the target node is found, delegate to a local
  `_delete` that handles four cases: (1) no right child -> return left
  subtree, (2) no left child -> return right subtree, (3) right child
  has no left child -> hoist right child up and graft left subtree onto
  it, (4) symmetric for left child with no right child, otherwise
  splice out the in-order successor (leftmost in right subtree), copy
  its value into the deleted node, and rewire its parent's left
  pointer. The parent's appropriate child pointer is replaced with the
  return value of `_delete`.
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

    def inorder(node):
        if not node:
            return []
        return inorder(node.left) + [node.val] + inorder(node.right)

    s = Solution()

    # Example 1: deleting 3 leaves a valid BST whose in-order traversal
    # is the original sorted set minus 3.
    r1 = s.deleteNode(build_tree([5, 3, 6, 2, 4, None, 7]), 3)
    assert inorder(r1) == [2, 4, 5, 6, 7]

    # Example 2: key not in tree -> tree unchanged (in-order unchanged).
    r2 = s.deleteNode(build_tree([5, 3, 6, 2, 4, None, 7]), 0)
    assert inorder(r2) == [2, 3, 4, 5, 6, 7]

    # Example 3: empty tree -> still empty.
    r3 = s.deleteNode(build_tree([]), 0)
    assert inorder(r3) == []

    print("detele_node_bst.py: all tests passed")
