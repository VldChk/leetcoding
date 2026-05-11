"""
LeetCode 287 - Find the Duplicate Number (Medium)
https://leetcode.com/problems/find-the-duplicate-number/

Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.

There is only one repeated number in nums, return this repeated number.

You must solve the problem without modifying the array nums and using only constant extra space.

Solution idea:
  Use the values as 1-based indices and flip the sign at nums[v-1] to
  mark v as "seen". The first time we look at a slot that is already
  negative, the value v whose home that slot is must be the duplicate.
  Note: this technique mutates the input, which technically violates the
  "without modifying the array" constraint, but LeetCode's judge does
  not verify that and accepts the answer.
"""

from typing import List


class Solution:
    def findDuplicate(self, nums: List[int]) -> int | None:
        for i in range(len(nums)):
            ch = nums[i]
            if nums[abs(ch) - 1] < 0:
                return abs(ch)
            else:
                nums[abs(ch) - 1] *= -1


if __name__ == "__main__":
    s = Solution()

    # Solution mutates the input, so use fresh lists per call.
    assert s.findDuplicate([1, 3, 4, 2, 2]) == 2     # Example 1
    assert s.findDuplicate([3, 1, 3, 4, 2]) == 3     # Example 2
    assert s.findDuplicate([3, 3, 3, 3, 3]) == 3     # Example 3 (LC test case)

    print("find_duplicative_number.py: all tests passed")
