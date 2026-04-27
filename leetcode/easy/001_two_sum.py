"""
LeetCode 1: Two Sum
https://leetcode.com/problems/two-sum/

Given an array of integers nums and an integer target, return indices of the
two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may
not use the same element twice.

Time Complexity: O(n)
Space Complexity: O(n)
"""
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i
        return []


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]

    # Test case 2
    assert solution.twoSum([3, 2, 4], 6) == [1, 2]

    # Test case 3
    assert solution.twoSum([3, 3], 6) == [0, 1]

    print("All test cases passed!")
