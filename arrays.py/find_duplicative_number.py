"""
Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive.

There is only one repeated number in nums, return this repeated number.

You must solve the problem without modifying the array nums and using only constant extra space.

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
