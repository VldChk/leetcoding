"""
LeetCode 2221 - Find Triangular Sum of an Array (Medium)
https://leetcode.com/problems/find-triangular-sum-of-an-array/

You are given a 0-indexed integer array nums, where nums[i] is a digit
between 0 and 9 (inclusive).

The triangular sum of nums is the value of the only element present in
nums after the following process terminates:

  - Let nums comprise n elements. If n == 1, terminate the process.
  - Otherwise, create a new 0-indexed integer array newNums of length
    n - 1, where newNums[i] = (nums[i] + nums[i+1]) % 10 for all
    0 <= i < n - 1.
  - Replace nums with newNums.

Return the triangular sum of nums.

Solution idea:
  In-place collapse. Each outer pass shrinks the live region by one;
  walk right-to-left within the region, summing each element with its
  *previous* (right-side) value and taking mod 10. By stashing the
  pre-update value in `prev` we never need extra arrays — the trailing
  positions become stale but are no longer read on subsequent passes
  (the range bound `len(nums)-j-1` shrinks each iteration). O(n^2) time,
  O(1) extra space.
"""


class Solution:
    def triangularSum(self, nums: list[int]) -> int:
        if len(nums) < 3:
            return sum(nums) % 10
        for j in range(1, len(nums)):
            prev = nums[-j]
            for i in range(len(nums)-j-1, -1, -1):
                new = nums[i]
                nums[i] = (nums[i] + prev) % 10
                prev = new
        return nums[0]


if __name__ == "__main__":
    s = Solution()

    # Solution mutates input; use fresh lists per call.
    assert s.triangularSum([1, 2, 3, 4, 5]) == 8         # Example 1
    assert s.triangularSum([5]) == 5                     # Example 2

    print("triangular_sum.py: all tests passed")
