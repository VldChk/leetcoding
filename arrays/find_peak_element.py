"""
LeetCode 162 - Find Peak Element (Medium)
https://leetcode.com/problems/find-peak-element/

A peak element is an element that is strictly greater than its
neighbors.

Given a 0-indexed integer array nums, find a peak element, and return
its index. If the array contains multiple peaks, return the index to
any of the peaks.

You may imagine that nums[-1] = nums[n] = -infinity. In other words,
an element is always considered to be strictly greater than a neighbor
that is outside the array.

You must write an algorithm that runs in O(log n) time.

Solution idea:
  Binary search with two early-exit shortcuts. Each iteration first
  cheaply checks whether the current `start_idx` is already a peak
  (its right neighbor is smaller) and whether `end_idx` is a peak
  (its left neighbor is smaller). Otherwise compare nums[mid] to
  nums[mid+1]: if descending, a peak lies in [start, mid]; if
  ascending, a peak lies in [mid+1, end]. The shortcuts cut off
  monotonic prefixes/suffixes faster than vanilla binary search but
  preserve the O(log n) bound.
"""
from typing import List

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        start_idx = 0
        end_idx = len(nums) - 1
        while start_idx < end_idx:
            if nums[start_idx + 1] < nums[start_idx]:
                return start_idx
            elif nums[end_idx - 1] < nums[end_idx]:
                return end_idx
            else:
                mid_idx = (start_idx + end_idx) // 2
                if nums[mid_idx] > nums[mid_idx + 1]:
                    end_idx = mid_idx
                else:
                    start_idx = mid_idx + 1
        return start_idx


if __name__ == "__main__":
    s = Solution()

    # Example 1: 3 is the unique peak at index 2.
    assert s.findPeakElement([1, 2, 3, 1]) == 2
    # Example 2: index 1 (value 2) and index 5 (value 6) are both valid peaks.
    assert s.findPeakElement([1, 2, 1, 3, 5, 6, 4]) in (1, 5)

    print("find_peak_element.py: all tests passed")
        