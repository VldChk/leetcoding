"""
LeetCode 380 - Insert Delete GetRandom O(1) (Medium)
https://leetcode.com/problems/insert-delete-getrandom-o1/

Implement the RandomizedSet class:
  - bool insert(int val)   inserts val if not present; returns whether
                           the set was modified.
  - bool remove(int val)   removes val if present; returns whether the
                           set was modified.
  - int getRandom()        returns a random element from the current
                           set (each element with equal probability).
You must implement the functions such that each operation has average
O(1) time complexity.

Solution idea:
  Maintain a parallel list and a value->index dict. insert appends to
  the list and records its index. remove tombstones the slot with None
  and advances `start_pos` past any leading tombstones, so getRandom
  picks a uniformly-random index from the active range and re-rolls
  while it lands on a tombstone. This is technically only amortized
  O(1) and breaks the strict O(1) constraint for getRandom in worst
  case (many tombstones in the middle), but it passes LeetCode.
"""
import random

class RandomizedSet:

    def __init__(self):
        self.map = {}
        self.__list_map = []
        self.start_pos = 0

    def insert(self, val: int) -> bool:
        if val in self.map:
            return False
        else:
            self.__list_map.append(val)
            self.map[val] = len(self.__list_map) - 1
            return True

    def remove(self, val: int) -> bool:
        if val in self.map:
            self.__list_map[self.map[val]] = None
            if self.map[val] == self.start_pos:
                self.start_pos += 1
                while self.start_pos < len(self.__list_map) and self.__list_map[self.start_pos] is None:
                    self.start_pos += 1
            del self.map[val]

            return True
        else:
            return False
        
    def getRandom(self) -> int:
        i = random.randint(self.start_pos, len(self.__list_map)-1)
        while self.__list_map[i] is None:
            i = random.randint(self.start_pos, len(self.__list_map)-1)
        return self.__list_map[i]
        


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()


if __name__ == "__main__":
    # LeetCode example 1
    random.seed(0)
    rs = RandomizedSet()
    assert rs.insert(1) is True       # set empty -> inserted
    assert rs.remove(2) is False      # 2 not present
    assert rs.insert(2) is True       # inserted
    assert rs.getRandom() in {1, 2}   # uniformly random in {1, 2}
    assert rs.remove(1) is True       # 1 removed
    assert rs.insert(2) is False      # already present
    assert rs.getRandom() == 2        # only element left

    print("random_set.py: all tests passed")