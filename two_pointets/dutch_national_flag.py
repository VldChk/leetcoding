"""
LeetCode 75 - Sort Colors (Medium)
https://leetcode.com/problems/sort-colors/

Given an array nums with n objects colored red, white, or blue, sort
them in-place so that objects of the same color are adjacent, with the
colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white,
and blue, respectively.

You must solve this problem without using the library's sort function.

Note: this file uses the Grokking-style name `sort(arr)` rather than
LeetCode's `sortColors(self, nums)`. The algorithm is identical (the
classic Dutch National Flag partition); only the method label differs.

Solution idea:
  Three pointers — start_idx (next slot for 0), end_idx (next slot for
  2), and i (scan head). Pre-skip any leading 0s and trailing 2s to
  shrink the working region. Then sweep: a 1 stays put, a 0 swaps to
  start_idx (and both advance), a 2 swaps to end_idx (which retracts;
  i stays put because the swapped-in value still needs inspection).
  O(n) single pass, O(1) extra space.
"""


class Solution:
    def sort(self, arr):
        start_idx = 0
        end_idx = len(arr) - 1
        while start_idx < len(arr) and arr[start_idx] == 0:
            start_idx += 1
        while end_idx >= 0 and arr[end_idx] == 2:
            end_idx -= 1
        i = start_idx
        while i <= end_idx:
            if arr[i] == 1:
                i += 1
                continue
            elif arr[i] == 0:
                arr[i], arr[start_idx] = arr[start_idx], arr[i]
                start_idx += 1
                i += 1
            else:
                arr[i], arr[end_idx] = arr[end_idx], arr[i]
                end_idx -= 1
        return arr


if __name__ == "__main__":
    s = Solution()

    assert s.sort([2, 0, 2, 1, 1, 0]) == [0, 0, 1, 1, 2, 2]   # Example 1
    assert s.sort([2, 0, 1]) == [0, 1, 2]                     # Example 2

    print("dutch_national_flag.py: all tests passed")
