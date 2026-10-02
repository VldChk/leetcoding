"""
LeetCode 494 - Target Sum (Medium)
https://leetcode.com/problems/target-sum/

Given an integer array nums and an integer target, put either '+' or '-'
in front of every element and concatenate them into an expression. Return
how many different sign assignments evaluate to target.

Example:
  nums = [1, 1, 1, 1, 1], target = 3 -> 5
    (-1+1+1+1+1, +1-1+1+1+1, +1+1-1+1+1, +1+1+1-1+1, +1+1+1+1-1)
  nums = [1], target = 1             -> 1

Solution idea:
  Depth-first search over the positions, carrying the running total. At the
  last index the two signs are checked directly and contribute 0, 1 or 2.
  The number of distinct running totals is bounded by the sum of nums
  (at most 1000), so memoising on (running total, index) collapses the
  2^n sign assignments into O(n * sum) states, each resolved in O(1).
  Duplicate values therefore cost nothing extra, and arrays containing
  zeroes still count both signs of a zero as distinct expressions, which
  is what the problem asks for.
"""
from typing import List


class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        memo = {}

        def _dfs(prev_val: int, curr_idx: int) -> int:
            if (prev_val, curr_idx) in memo:
                return memo[(prev_val, curr_idx)]

            positive = prev_val + nums[curr_idx]
            negative = prev_val - nums[curr_idx]
            if curr_idx == len(nums) - 1:
                cnt = (positive == target) + (negative == target)
            else:
                cnt = _dfs(positive, curr_idx + 1) + _dfs(negative, curr_idx + 1)

            memo[(prev_val, curr_idx)] = cnt
            return cnt
        return _dfs(0, 0)


if __name__ == "__main__":
    s = Solution()

    # Official examples
    assert s.findTargetSumWays([1, 1, 1, 1, 1], 3) == 5
    assert s.findTargetSumWays([1], 1) == 1
    # Zeroes: +0 and -0 count as different expressions
    assert s.findTargetSumWays([0, 0, 0], 0) == 8

    print("target_sum.py: all tests passed")
