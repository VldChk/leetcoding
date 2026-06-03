"""
LeetCode 41 — First Missing Positive (Hard)
https://leetcode.com/problems/first-missing-positive/

Given an unsorted integer array `nums`, return the smallest positive integer
that is NOT present in `nums`. Must run in O(n) time and use O(1) auxiliary space.

Examples:
    [1,2,0]      -> 3
    [3,4,-1,1]   -> 2
    [7,8,9,11,12]-> 1

Idea — cyclic sort (in-place index→value mapping):
The answer is in [1..n+1]. Walk the array and for each i, if nums[i] is in [1..n]
and not already in its "home slot" (idx == nums[i]-1), swap it there. Values out
of range or already-placed are skipped. A second pass returns the first i where
nums[i] != i+1; if all match, the answer is n+1.

Complexity:
    Time  O(n) — each element gets placed at most once; the inner loop is amortised
    Space O(1)
"""
from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:

        if len(nums) == 1:
            return 1 if nums[0] != 1 else 2
        
        i = 0
        while i < len(nums):
            if i == nums[i] - 1:
                i += 1
                continue
            elif nums[i] < 1 or nums[i] > len(nums):
                i += 1
                continue
            else:
                next_idx = nums[i]
                while not (next_idx < 1 or next_idx > len(nums)) and next_idx != nums[next_idx-1]:
                    t = nums[next_idx-1]
                    nums[next_idx-1] = next_idx
                    next_idx = t
                i += 1

        for i in range(len(nums)):
            if i != nums[i]-1:
                return i+1

        return len(nums) + 1


if __name__ == "__main__":
    sol = Solution()
    assert sol.firstMissingPositive([1, 2, 0]) == 3
    assert sol.firstMissingPositive([3, 4, -1, 1]) == 2
    assert sol.firstMissingPositive([7, 8, 9, 11, 12]) == 1
    assert sol.firstMissingPositive([1]) == 2
    assert sol.firstMissingPositive([2]) == 1
    assert sol.firstMissingPositive([1, 2, 3, 4, 5]) == 6
    print("missing_positive_integer.py: all tests passed")