"""
LeetCode 167 - Two Sum II - Input Array Is Sorted (Medium)
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

Given a 1-indexed array of integers numbers that is already sorted in
non-decreasing order, find two numbers such that they add up to a
specific target number.

Return the indices of the two numbers, index1 and index2, added by one
as an integer array [index1, index2] of length 2.

The tests are generated such that there is exactly one solution. You
may not use the same element twice.

Your solution must use only constant extra space.

Solution idea:
  Two pointers from both ends. The bisect-based jump (instead of
  stepping one at a time) accelerates skip-over of values that are
  obviously too large or too small: when the sum overshoots target,
  jump j to bisect(numbers, target - numbers[i]) - 1; when it
  undershoots, jump i to bisect_left(numbers, target - numbers[j]).
  Faster than naive ±1 stepping on inputs with large gaps; same O(n)
  worst case but much less work in practice.
"""
from bisect import bisect, bisect_left
from typing import List
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i = 0
        j = len(numbers) - 1
        while i < j:
            if numbers[i] + numbers[j] == target:
                return [i+1, j+1]
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

    assert s.twoSum([2, 7, 11, 15], 9) == [1, 2]    # Example 1
    assert s.twoSum([2, 3, 4], 6) == [1, 3]         # Example 2
    assert s.twoSum([-1, 0], -1) == [1, 2]          # Example 3

    print("two_sum_sorted.py: all tests passed")
