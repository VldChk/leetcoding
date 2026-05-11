"""
LeetCode 1 - Two Sum (Easy)
https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices
of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and
you may not use the same element twice. You can return the answer in
any order.

Solution idea (the "unorthodox" sorted+bisect variant):
  Make a sorted copy of nums and run two pointers from both ends. When
  the pair sum overshoots/undershoots, jump the pointer with bisect
  rather than stepping by one — `bisect`/`bisect_left` snap directly to
  the position of (target - opposite). When the sum hits, translate the
  values back to original indices via `nums.index`, taking care to
  skip the first when both values are the same number (avoid returning
  the same index twice). Runs in O(n log n) for the sort plus log n
  per jump.
"""
from bisect import bisect, bisect_left
from typing import List
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numbers = sorted(nums)
        i = 0
        j = len(numbers) - 1
        while i < j:
            if numbers[i] + numbers[j] == target:
                idx_i = nums.index(numbers[i])
                if numbers[i] == numbers[j]:
                    idx_j = nums.index(numbers[j], idx_i+1)
                else:
                    idx_j = nums.index(numbers[j])
                return [idx_i, idx_j]
            elif numbers[i] + numbers[j] > target:
                opposite = target - numbers[i]
                idx = bisect(numbers, opposite)
                j = idx-1
            else:
                opposite = target - numbers[j]
                idx = bisect_left(numbers, opposite)
                i = idx
        return [-1, -1]


if __name__ == "__main__":
    s = Solution()

    # LeetCode accepts any order of the two indices.
    assert sorted(s.twoSum([2, 7, 11, 15], 9)) == [0, 1]    # Example 1
    assert sorted(s.twoSum([3, 2, 4], 6)) == [1, 2]         # Example 2
    assert sorted(s.twoSum([3, 3], 6)) == [0, 1]            # Example 3

    print("2s_unorthodox.py: all tests passed")