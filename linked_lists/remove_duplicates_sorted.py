"""
LeetCode 83 - Remove Duplicates from Sorted List (Easy)
https://leetcode.com/problems/remove-duplicates-from-sorted-list/

Given the head of a sorted linked list, delete all duplicates such that
each element appears only once. Return the linked list sorted as well.

Solution idea:
  Single pass with two pointers (prev_node, node). Walk the list; while
  node.val matches prev_node.val, drop node by advancing past it without
  updating prev_node and remember `prev_the_same` so we know to relink
  when we land on a different value. When the values differ, splice the
  preserved prev_node directly to the new node (skipping the run of
  duplicates) and shift prev_node forward. After the scan, if the tail
  ended on a duplicate run, terminate prev_node.next at None.
"""


# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def deleteDuplicates(self, head):
        """
        :type head: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        if not head:
            return
        node = head.next
        prev_node = head
        prev_the_same = False
        while node:
            if node.val == prev_node.val:
                prev_the_same = True
                node = node.next
            else:
                if prev_the_same:
                    prev_node.next = node
                prev_the_same = False
                prev_node = node
                node = node.next
        if prev_the_same:
            prev_node.next = None
        return head


if __name__ == "__main__":
    def to_list(head):
        out = []
        while head:
            out.append(head.val)
            head = head.next
        return out

    def from_list(values):
        head = None
        for v in reversed(values):
            head = ListNode(v, head)
        return head

    s = Solution()

    # Example 1: 1 -> 1 -> 2 becomes 1 -> 2
    assert to_list(s.deleteDuplicates(from_list([1, 1, 2]))) == [1, 2]
    # Example 2: 1 -> 1 -> 2 -> 3 -> 3 becomes 1 -> 2 -> 3
    assert to_list(s.deleteDuplicates(from_list([1, 1, 2, 3, 3]))) == [1, 2, 3]

    print("remove_duplicates_sorted.py: all tests passed")
