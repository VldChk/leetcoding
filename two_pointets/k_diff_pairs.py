"""
LeetCode 532 - K-diff Pairs in an Array (Medium)
https://leetcode.com/problems/k-diff-pairs-in-an-array/

Given an array of integers nums and an integer k, return the number of
unique k-diff pairs in the array.

A k-diff pair is an integer pair (nums[i], nums[j]), where the
following are true:
  - 0 <= i, j < nums.length
  - i != j
  - |nums[i] - nums[j]| == k

Notice that |val| denotes the absolute value of val.

Solution idea:
  Sort, then run two pointers (i < j). When |nums[i] - nums[j]| == k,
  count the pair, then skip duplicates of nums[i] and nums[j] before
  advancing j. When the difference is too small, j moves right; too
  large, i moves right. The duplicate-skip is what makes the count
  "unique pairs" rather than "all pairs".
"""
from typing import List
class Solution:
    def findPairs(self, nums: List[int], k: int) -> int:
        nums.sort()
        if len(nums) < 2:
            return 0
        i = 0
        j = 1
        cnt = 0
        while i < j and j < len(nums):
            if abs(nums[i] - nums[j]) == k:
                cnt += 1
                while i+1 < j and nums[i+1] == nums[i]:
                    i += 1
                while j+1 < len(nums) and nums[j+1] == nums[j]:
                    j += 1
                j += 1
            elif abs(nums[i] - nums[j]) < k:
                j += 1
            else:
                i += 1
            if i == j:
                j += 1
        return cnt


if __name__ == "__main__":
    s = Solution()

    assert s.findPairs([3, 1, 4, 1, 5], 2) == 2           # Example 1
    assert s.findPairs([1, 2, 3, 4, 5], 1) == 4           # Example 2
    assert s.findPairs([1, 3, 1, 5, 4], 0) == 1           # Example 3

    print("k_diff_pairs.py: all tests passed")
        