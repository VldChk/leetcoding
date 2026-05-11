"""
LeetCode 381 - Insert Delete GetRandom O(1) - Duplicates allowed (Hard)
https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/

Like LC 380, but the multiset variant: duplicates are permitted, and
getRandom must return each element with probability proportional to its
frequency in the collection.

Implement the RandomizedCollection class:
  - bool insert(int val)  inserts an item; returns True iff this was the
                          first time val was inserted.
  - bool remove(int val)  removes one occurrence of val; returns True
                          iff val was present.
  - int getRandom()       returns a random element with probability
                          proportional to its current count.

Solution idea:
  Same backing list + tombstone scheme as LC 380, but the dict stores
  a list of indices per value (one per occurrence). insert appends and
  pushes the new index. remove tombstones the slot at the head index
  for that value and pops it from the list; if no occurrences remain,
  the dict entry is deleted. getRandom rolls a uniform index in the
  active range and re-rolls past tombstones — the probability is
  proportional to count because each occurrence has its own list slot.
"""
import random

class RandomizedCollection:

    def __init__(self):
        self.map = {}
        self.__list_map = []
        self.start_pos = 0

    def insert(self, val: int) -> bool:
        if val in self.map:
            self.__list_map.append(val)
            self.map[val].append(len(self.__list_map) - 1)
            return False
        else:
            self.__list_map.append(val)
            self.map[val] = [len(self.__list_map) - 1]
            return True

    def remove(self, val: int) -> bool:
        if val in self.map:
            self.__list_map[self.map[val][0]] = None
            if self.map[val][0] == self.start_pos:
                self.start_pos += 1
                while self.start_pos < len(self.__list_map) and self.__list_map[self.start_pos] is None:
                    self.start_pos += 1
            self.map[val].pop(0)
            if len(self.map[val]) == 0:
                del self.map[val]

            return True
        else:
            return False
        
    def getRandom(self) -> int:
        i = random.randint(self.start_pos, len(self.__list_map)-1)
        while self.__list_map[i] is None:
            i = random.randint(self.start_pos, len(self.__list_map)-1)
        return self.__list_map[i]
        


# Your RandomizedCollection object will be instantiated and called as such:
# obj = RandomizedCollection()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()


if __name__ == "__main__":
    # LeetCode example 1
    random.seed(0)
    rc = RandomizedCollection()
    assert rc.insert(1) is True       # 1 not yet present
    assert rc.insert(1) is False      # 1 already present (now twice)
    assert rc.insert(2) is True       # 2 not yet present
    assert rc.getRandom() in {1, 2}   # 1 with p=2/3, 2 with p=1/3
    assert rc.remove(1) is True       # one copy of 1 removed
    assert rc.getRandom() in {1, 2}   # 1 and 2 each with p=1/2

    print("random_set_duplicate.py: all tests passed")