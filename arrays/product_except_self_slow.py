"""
LeetCode 238 - Product of Array Except Self (Medium)
https://leetcode.com/problems/product-of-array-except-self/

Given an integer array `nums`, return an array `answer` such that
`answer[i]` is the product of all elements of `nums` except `nums[i]`.

You must write the algorithm without using the division operation.

Solution idea (the "slow" variant):
  - First handle zeros explicitly: 2+ zeros -> all zeros; exactly one
    zero -> only that index gets the product of the non-zeros.
  - Otherwise, group equal values into a dict mapping value -> (running
    product across all occurrences, product across previous occurrences
    only). For each index, multiply together the "all-occurrences"
    products of every other distinct value, then multiply by the
    "previous-occurrences" product of nums[i] itself. That yields the
    product of all elements except nums[i].
  Correct but O(n * unique) per index — slower than the prefix/suffix
  trick.
"""
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        import math
        zeroes = [0 for i in nums if i == 0]
        if len(zeroes) > 1:
            return [0] * len(nums)
        elif len(zeroes) == 1:
            non_zero = math.prod([i for i in nums if i != 0])
            return [non_zero if i == 0 else 0 for i in nums]
        
        d: dict[int, tuple[int, int]] = {}

        for n in nums:
            if n in d:
                curr = d[n][0]
                nxt = curr * n
                d[n] = (nxt, curr)
            else:
                d[n] = (n, 1)
        
        for i, n in enumerate(nums):
            pre_compute = math.prod([v[0] for k, v in d.items() if k != n])
            pre_compute *= d[n][1]
            nums[i] = pre_compute

        return nums


if __name__ == "__main__":
    s = Solution()

    # Solution mutates the input list, so use fresh lists per call.
    assert s.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]            # Example 1
    assert s.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]      # Example 2

    print("product_except_self_slow.py: all tests passed")
        