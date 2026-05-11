
"""
LeetCode 238 - Product of Array Except Self (Medium)
https://leetcode.com/problems/product-of-array-except-self/

Given an integer array `nums`, return an array `answer` such that
`answer[i]` is the product of all elements of `nums` except `nums[i]`.

The product of any prefix or suffix of `nums` is guaranteed to fit in a
32-bit integer. You must write an algorithm that runs in O(n) time and
without using the division operation.

Solution idea (the "fast" variant):
  Two passes, no extra arrays beyond the output. First pass: fill `res`
  with prefix products (res[i] = product of nums[:i]). Second pass: walk
  right-to-left maintaining a running suffix product and multiply it
  into res[i]. Final res[i] = prefix(i) * suffix(i) = product of all
  elements except nums[i]. O(n) time, O(1) auxiliary space.
"""
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        for i in range(1, len(nums)):
            res[i] = res[i-1] * nums[i-1]
        
        right_cumulative = 1
        for j in range(len(nums)-1, -1, -1):
            res[j] = res[j] * right_cumulative
            right_cumulative = right_cumulative * nums[j]

        return res


if __name__ == "__main__":
    s = Solution()

    assert s.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]              # Example 1
    assert s.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]        # Example 2

    print("product_except_self_fast.py: all tests passed")