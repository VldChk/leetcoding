"""
LeetCode 2958 - Length of Longest Subarray With at Most K Frequency (Medium)
https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/

An array is good when every value in it occurs at most k times. Given an
integer array nums and an integer k, return the length of the longest good
subarray (a contiguous, non-empty stretch of nums).

Example:
  nums = [1, 2, 3, 1, 2, 3, 1, 2], k = 2 -> 6   ([1,2,3,1,2,3])
  nums = [1, 2, 1, 2, 1, 2, 1, 2], k = 1 -> 2   ([1,2])
  nums = [5, 5, 5, 5, 5, 5, 5],    k = 4 -> 4   ([5,5,5,5])

Solution idea:
  Sliding window with a frequency map. Extending the window to the right is
  free until the incoming value already appears k times; at that point the
  window just before it is a candidate answer, so record its length, then
  advance the left edge — dropping counts as it goes — until that value
  falls below k and the new element fits. Each index enters and leaves the
  window once, and the final window is measured after the loop, so the
  whole scan is O(n) time and O(distinct values) space.
"""
from typing import List


class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        if len(nums) < 2:
            return len(nums)
        freq = {}

        res = 0
        right = 0
        left = 0

        for i, val in enumerate(nums):
            right = i
            if val not in freq:
                freq[val] = 1
                continue
            elif freq[val] < k:
                freq[val] += 1
                continue
            else:
                res = max(res, right - left)
                while freq[val] == k:
                    freq[nums[left]] -= 1
                    left += 1
                freq[val] += 1
        return max(res, right - left + 1)


if __name__ == "__main__":
    s = Solution()

    # Official examples
    assert s.maxSubarrayLength([1, 2, 3, 1, 2, 3, 1, 2], 2) == 6
    assert s.maxSubarrayLength([1, 2, 1, 2, 1, 2, 1, 2], 1) == 2
    assert s.maxSubarrayLength([5, 5, 5, 5, 5, 5, 5], 4) == 4

    print("longest_subarray_with_k.py: all tests passed")
