"""
LeetCode 33 - Search in Rotated Sorted Array (Medium)
https://leetcode.com/problems/search-in-rotated-sorted-array/

There is an integer array nums sorted in ascending order (with
distinct values). Prior to being passed to your function, nums is
possibly rotated at an unknown pivot index k (1 <= k < nums.length)
such that the resulting array is
[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]
(0-indexed).

Given the array nums after the possible rotation and an integer
target, return the index of target if it is in nums, or -1 if it is
not in nums. You must write an algorithm with O(log n) runtime.

Solution idea:
  Two-phase binary search. Phase 1: locate the rotation pivot index
  (same routine as LC 153). Phase 2: do a standard binary search on
  the logical-sorted view by adding the pivot offset to every index
  and reducing modulo n via the `normalize` lambda — this lets the
  search treat the array as if it were sorted ascending, while
  reading from its rotated physical layout. Both phases are O(log n).
"""
from typing import List, Callable

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        if len(nums) < 2:
            return 0 if target in nums else -1
        if nums[0] > nums[-1]:
            rotated = True
            rotation_bias = None
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

        normalize: Callable[[int], int] = lambda x: x - len(nums)*(x//len(nums))

        start_idx = rotation_bias
        end_idx = len(nums) - 1 + rotation_bias

        while start_idx <= end_idx:
            if start_idx == end_idx:
                if nums[normalize(start_idx)] == target:
                    return normalize(start_idx)
                else:
                    return -1
            else:
                mid_idx = (start_idx + end_idx) // 2
                if nums[normalize(mid_idx)] == target:
                    return normalize(mid_idx)
                elif nums[normalize(mid_idx)] < target:
                    start_idx = mid_idx + ((start_idx + end_idx) % 2)
                else:
                    end_idx = mid_idx

        return -1


if __name__ == "__main__":
    s = Solution()

    assert s.search([4, 5, 6, 7, 0, 1, 2], 0) == 4         # Example 1
    assert s.search([4, 5, 6, 7, 0, 1, 2], 3) == -1         # Example 2
    assert s.search([1], 0) == -1                            # Example 3

    print("search_in_rotated_array.py: all tests passed")
