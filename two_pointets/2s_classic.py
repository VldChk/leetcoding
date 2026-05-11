"""
LeetCode 1 - Two Sum (Easy)
https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices
of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and
you may not use the same element twice. You can return the answer in
any order.

Solution idea (the "classic" hash-map version):
  Single pass. For each element n at index i, check whether (target - n)
  has been seen before in the dict. If yes, we have a pair: return the
  earlier index plus i. Otherwise stash n -> i and move on. O(n) time
  and O(n) space.
"""
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = {}
        for i, n in enumerate(nums):
            if target - n in d:
                return [d[target - n], i]
            else:
                d[n] = i
        return []


if __name__ == "__main__":
    s = Solution()

    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]    # Example 1
    assert s.twoSum([3, 2, 4], 6) == [1, 2]         # Example 2
    assert s.twoSum([3, 3], 6) == [0, 1]            # Example 3

    print("2s_classic.py: all tests passed")