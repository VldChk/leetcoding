"""
LeetCode 153 - Find Minimum in Rotated Sorted Array (Medium)
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/

Suppose an array of length n sorted in ascending order is rotated
between 1 and n times. Given the sorted rotated array nums of unique
elements, return the minimum element of this array.

You must write an algorithm that runs in O(log n) time.

Solution idea:
  If nums[0] <= nums[-1], the array isn't rotated — the minimum is
  nums[0]. Otherwise, binary-search for the rotation pivot: at each
  step compare nums[mid] with nums[end]. If nums[mid] > nums[end], the
  pivot is strictly to the right of mid, so move start past mid; else
  the pivot is at or before mid, shrink end to mid. Converges to the
  pivot index (which is also the index of the global minimum).
  O(log n).
"""
from typing import List
class Solution:
    def findMin(self, nums: List[int]) -> int:
        if len(nums) < 2:
            return nums[0]
        if nums[0] > nums[-1]:
            rotated = True
            rotation_bias = -1
        else:
            rotated = False
            rotation_bias = 0

        if rotated:
            start_idx = 0
            end_idx = len(nums) - 1
            while start_idx <= end_idx:
                if start_idx == end_idx:
                    rotation_bias = start_idx
                    break
                else:
                    mid_idx = (start_idx + end_idx) // 2
                    if nums[mid_idx] > nums[end_idx]:
                        start_idx = mid_idx + ((start_idx + end_idx) % 2)
                    else:
                        end_idx = mid_idx
            return nums[rotation_bias]
        else:
            return nums[0]


if __name__ == "__main__":
    s = Solution()

    assert s.findMin([3, 4, 5, 1, 2]) == 1                  # Example 1
    assert s.findMin([4, 5, 6, 7, 0, 1, 2]) == 0             # Example 2
    assert s.findMin([11, 13, 15, 17]) == 11                 # Example 3 (no rotation)

    print("min_in_rotated_array.py: all tests passed")
