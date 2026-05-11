"""
LeetCode 170 - Two Sum III - Data structure design (Easy, Premium)
https://leetcode.com/problems/two-sum-iii-data-structure-design/

Design a data structure that accepts a stream of integers and checks
if it has a pair of integers that sum up to a particular value.

Implement the TwoSum class:
  - TwoSum()             Initializes the TwoSum object.
  - void add(int number) Adds number to the data structure.
  - boolean find(value)  Returns true if there exists any pair of
                         numbers whose sum is equal to value, false
                         otherwise.

Solution idea:
  Keep numbers in a sorted list (`bisect.insort_left` on `add`). On
  `find`, run two pointers from both ends — classic two-sum-on-sorted.
  O(log n) on add (insort moves elements but the search is log n) and
  O(n) on find. A different trade-off than the dict-based variant
  (O(1) add, O(n) find both); LC accepts either.
"""
import bisect


class TwoSum(object):

    def __init__(self):
        self.arr = []

    def add(self, number):
        """
        :type number: int
        :rtype: None
        """
        bisect.insort_left(self.arr, number)

    def _find_pair(self, number):
        start_idx = 0
        end_idx = len(self.arr) - 1
        while start_idx < end_idx:
            if self.arr[start_idx] + self.arr[end_idx] > number:
                end_idx -= 1
            elif self.arr[start_idx] + self.arr[end_idx] < number:
                start_idx += 1
            else:
                return True
        return False

    def find(self, value):
        """
        :type value: int
        :rtype: bool
        """
        return self._find_pair(value)


# Your TwoSum object will be instantiated and called as such:
# obj = TwoSum()
# obj.add(number)
# param_2 = obj.find(value)


if __name__ == "__main__":
    # LeetCode example 1
    ts = TwoSum()
    ts.add(1)
    ts.add(3)
    ts.add(5)
    assert ts.find(4) is True       # 1 + 3 = 4
    assert ts.find(7) is False      # no pair sums to 7

    print("two_sum_ds.py: all tests passed")
