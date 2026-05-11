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

Solution idea (this file: dict-only variant):
  Lean on the fact that Python 3.7+ dicts preserve *insertion order*.
  The least-recently-used key is whichever was inserted earliest, i.e.
  `next(iter(self.cache))`. To "touch" a key (mark it most-recently
  used) we delete and re-insert it, sending it to the back. Eviction
  pops the front. This avoids the explicit doubly-linked list of the
  sibling `lru_cache.py` at the cost of relying on a CPython
  implementation guarantee — which has been part of the language spec
  since 3.7, so the trade is fine for LeetCode and modern Python.
"""


class LRUCache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache: dict[int, int] = {}
    
    def _remove_last_node(self) -> None:
        if len(self.cache) > 1:
            lru_key = next(iter(self.cache))
            del self.cache[lru_key]
        else:
            self.cache = {}
    
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        
        val = self.cache[key]
        del self.cache[key]
        self.cache[key] = val
        return val
        
    
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            del self.cache[key]
            self.cache[key] = value
        else:
            self.cache[key] = value
            
            if len(self.cache) > self.capacity:
                self._remove_last_node()


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

    print("lru_cache_dict.py: all tests passed")
