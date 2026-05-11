"""
LeetCode 146 - LRU Cache (Medium)
https://leetcode.com/problems/lru-cache/

Design a data structure that follows the constraints of a Least
Recently Used (LRU) cache.

Implement the LRUCache class:
  - LRUCache(int capacity)        Initializes the LRU cache with positive
                                   size capacity.
  - int get(int key)              Returns the value of the key if it
                                   exists, otherwise returns -1.
  - void put(int key, int value)  Updates the value of the key if it
                                   exists. Otherwise, adds the key-value
                                   pair. If the number of keys exceeds
                                   capacity, evict the least recently
                                   used key.

Both get and put must run in O(1) average time complexity.

Solution idea:
  Doubly-linked list (most-recently-used at head, least at tail) plus a
  dict mapping key -> node for O(1) lookup. `get` finds the node, splices
  it out, and re-inserts it at the head. `put` either replaces an
  existing node (move-to-head semantics again) or appends a new one,
  evicting the tail neighbour when over capacity.

Typing note:
  Each `Node` initialises `_next` / `_prev` to `self` (self-reference),
  so the field type stays `Node` (not `Optional[Node]`) without any
  infinite recursion. LinkedList wires up real prev/next pointers
  immediately after construction. Sentinel head and tail keep their
  outward pointers self-looped (head.prev == head, tail.next == tail),
  which keeps every accessor's return type as `Node` and avoids the
  pyre cascade you hit with `Optional[Node]` (where
  `prev_node.prev = node` complains that prev_node could be None).
"""
from __future__ import annotations


class Node:
    def __init__(self, key: int, val: int) -> None:
        self.__val = val
        self.__key = key
        # Self-reference avoids the `Optional[Node]` cascade in pyre
        # while never triggering infinite recursion at construction
        # (a name binding is not a constructor call). The owning
        # LinkedList rewires real prev/next pointers right away.
        self._next: Node = self
        self._prev: Node = self

    @property
    def next(self) -> Node:
        return self._next

    @next.setter
    def next(self, node: Node) -> None:
        self._next = node

    @property
    def prev(self) -> Node:
        return self._prev

    @prev.setter
    def prev(self, node: Node) -> None:
        self._prev = node

    @property
    def key(self) -> int:
        return self.__key

    @property
    def val(self) -> int:
        return self.__val


class LinkedList:
    def __init__(self) -> None:
        self.head: Node = Node(-1, -1)
        self.tail: Node = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head

    def add_node_next_to_head(self, node: Node) -> None:
        prev_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = prev_node
        prev_node.prev = node

    def delete_node(self, node: Node) -> None:
        next_node = node.next
        prev_node = node.prev
        next_node.prev = prev_node
        prev_node.next = next_node

    def delete_last_node(self) -> None:
        last_node = self.tail.prev
        if last_node is self.head:
            return
        else:
            self.delete_node(last_node)
        

class LRUCache(object):

    def __init__(self, capacity: int) -> None:
        """
        :type capacity: int
        """
        self.lru_list = LinkedList()
        self.capacity = capacity
        self.lru: dict[int, Node] = {}
        

    def get(self, key: int) -> int:
        """
        :type key: int
        :rtype: int
        """
        # print(self.lru_list)
        if key not in self.lru:
            return -1
        else:
            node = self.lru[key]
            self.lru_list.delete_node(node)
            self.lru_list.add_node_next_to_head(node)
            return node.val
        

    def put(self, key: int, value: int) -> None:
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        # print(self.lru_list)
        new_node = Node(key, value)
        self.lru_list.add_node_next_to_head(new_node)
        if key in self.lru:
            old_node = self.lru[key]
            self.lru_list.delete_node(old_node)
            self.lru[key] = new_node
        else:
            if len(self.lru) >= self.capacity:
                last_node = self.lru_list.tail.prev
                del self.lru[last_node.key]
                self.lru_list.delete_node(last_node)
            self.lru[key] = new_node
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)


if __name__ == "__main__":
    # LeetCode example 1
    c = LRUCache(2)
    c.put(1, 1)                     # cache = {1=1}
    c.put(2, 2)                     # cache = {1=1, 2=2}
    assert c.get(1) == 1            # touches 1; LRU order is now {2, 1}
    c.put(3, 3)                     # evicts 2; cache = {1=1, 3=3}
    assert c.get(2) == -1           # 2 was evicted
    c.put(4, 4)                     # evicts 1; cache = {3=3, 4=4}
    assert c.get(1) == -1           # 1 was evicted
    assert c.get(3) == 3
    assert c.get(4) == 4

    print("lru_cache.py: all tests passed")