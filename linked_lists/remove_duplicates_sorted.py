"""
Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.
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
