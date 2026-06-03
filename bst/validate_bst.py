"""
LeetCode 98 — Validate Binary Search Tree (Medium)
https://leetcode.com/problems/validate-binary-search-tree/

Given the root of a binary tree, determine whether it is a valid BST:
the entire left subtree is strictly less than the node, the entire right
subtree is strictly greater, and both subtrees are themselves valid BSTs.

Examples:
    [2,1,3]               -> True
    [5,1,4,null,null,3,6] -> False (right child 4 < root 5)

Idea — bounds passed down the recursion:
For each node, maintain (lower, upper) that the value must lie strictly inside.
When recursing left, tighten upper to min(upper, node.val); when recursing right,
loosen lower to max(lower, node.val). A failed bound check returns False without
exploring further (early prune).

Complexity:
    Time  O(n)
    Space O(h) recursion stack, h = tree height
"""
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isValidBST(self, root: TreeNode, smaller_than: int = 2**31, bigger_than: int = -2**31-1) -> bool:
        is_valid = True
        if root.left:
            if root.left.val < root.val and root.left.val < smaller_than and root.left.val > bigger_than:
                is_valid = self.isValidBST(root.left, min(smaller_than, root.val), bigger_than)
            else:
                return False
        
        if root.right and is_valid:
            if root.right.val > root.val and root.right.val < smaller_than and root.right.val > bigger_than:
                is_valid = self.isValidBST(root.right, smaller_than,  max(bigger_than, root.val))
            else:
                return False

        return is_valid


if __name__ == "__main__":
    def build(vals):
        """Level-order builder. None means absent."""
        if not vals:
            return None
        it = iter(vals)
        root = TreeNode(next(it))
        queue = [root]
        for v in it:
            parent = queue[0]
            slot = next(it, "__missing__")
            if v is not None:
                parent.left = TreeNode(v)
                queue.append(parent.left)
            if slot != "__missing__" and slot is not None:
                parent.right = TreeNode(slot)
                queue.append(parent.right)
            queue.pop(0)
        return root

    sol = Solution()
    # Example 1: [2,1,3] -> True
    assert sol.isValidBST(build([2, 1, 3])) is True
    # Example 2: [5,1,4,null,null,3,6] -> False
    assert sol.isValidBST(build([5, 1, 4, None, None, 3, 6])) is False
    # Single node
    assert sol.isValidBST(TreeNode(1)) is True
    # Right child equal to root -> not strictly greater -> False
    root = TreeNode(1, None, TreeNode(1))
    assert sol.isValidBST(root) is False
    # Deeper invalid: left subtree contains a value >= ancestor
    # [10, 5, 15, null, null, 6, 20] — 6 < 10 but lives in right subtree of 10
    assert sol.isValidBST(build([10, 5, 15, None, None, 6, 20])) is False
    print("validate_bst.py: all tests passed")
