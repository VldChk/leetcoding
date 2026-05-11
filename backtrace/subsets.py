"""
LeetCode 78 - Subsets (Medium)
https://leetcode.com/problems/subsets/

Given an integer array `nums` of unique elements, return all possible
subsets (the power set). The solution set must not contain duplicate
subsets. Return the answer in any order.

Solution idea:
  Backtracking. Seed `res` with the empty subset. The recursive
  `_backtrace(prefix, remaining, res)` walks the remaining list; at each
  index i it appends `prefix + [remaining[i]]` to the answer and recurses
  into the suffix `remaining[i+1:]`, so each element is either taken
  exactly once at the position it appears or skipped, generating every
  subset without duplicates.
"""
from typing import List


class Solution:

    def subsets(self, nums: List[int]) -> List[List[int]]:
        def _backtrace(it: List[int], nums: List[int], res: List[List[int]]):
            for i in range(len(nums)):
                t = it + [nums[i]]
                res.append(t)
                if i == len(nums) - 1:
                    return
                _backtrace(t, nums[i + 1 :], res)
            return res

        res = [[]]
        it = []
        i = 2
        _backtrace(it, nums, res)
        return res


if __name__ == "__main__":
    s = Solution()

    def normalize(subsets):
        # LeetCode accepts subsets in any order, and elements within each
        # subset in any order. Normalize for comparison.
        return sorted(sorted(sub) for sub in subsets)

    assert normalize(s.subsets([1, 2, 3])) == normalize(
        [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]
    )                                                                   # Example 1
    assert normalize(s.subsets([0])) == normalize([[], [0]])            # Example 2

    print("subsets.py: all tests passed")
