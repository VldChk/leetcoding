
"""
LeetCode 442 - Find All Duplicates in an Array (Medium)
https://leetcode.com/problems/find-all-duplicates-in-an-array/

Given an integer array `nums` of length n where all integers are in the
range [1, n] and each integer appears at most twice, return an array of
all the integers that appear twice.

You must write an algorithm that runs in O(n) time and uses only constant
auxiliary space (the output array does not count).

Solution idea:
  Cyclic sort, in place. Decrement values to 0-based so each value should
  live at index == value. Walk the array; if `nums[i] != i`, place its
  value home by chasing the cycle: at each step, write `t` into `nums[t]`
  and pick up the displaced value as the new `t`. When we land on a slot
  whose value already equals `t`, the current `t` has already been placed
  -> it's the duplicate. Cleared slots are marked -1 to terminate cycles.
"""
from typing import List
class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        i = 0
        dups: List[int] = []
        nums = [i-1 for i in nums]
        for i, n in enumerate(nums):
            if n == i:
                continue
            else:
                nums[i] = -1
                t = n
                while True:
                    if nums[t] == t:
                        dups.append(t)
                        break
                    else:
                        nums[t], t = t, nums[t]
                        if t == -1:
                            break

        return [d+1 for d in dups]


if __name__ == "__main__":
    s = Solution()

    # LeetCode accepts duplicates in any order, so compare via sorted().
    assert sorted(s.findDuplicates([4, 3, 2, 7, 8, 2, 3, 1])) == [2, 3]   # Example 1
    assert sorted(s.findDuplicates([1, 1, 2])) == [1]                     # Example 2
    assert sorted(s.findDuplicates([1])) == []                            # Example 3

    print("find_all_duplicates.py: all tests passed")
