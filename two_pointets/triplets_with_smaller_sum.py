"""
LeetCode 259 - 3Sum Smaller (Medium, Premium)
https://leetcode.com/problems/3sum-smaller/

Given an array of n integers nums and an integer target, find the
number of index triplets i, j, k with 0 <= i < j < k < n that satisfy
the condition nums[i] + nums[j] + nums[k] < target.

Note: this file uses the Grokking-style name `searchTriplets(arr,
target)` rather than LeetCode's `threeSumSmaller(self, nums, target)`.
The algorithm is identical; only the method label differs.

Solution idea:
  Sort. Fix the leftmost element n at index i. For the remaining suffix
  run two pointers; when n + arr[start] + arr[end] < target, every
  pair (start, k) for k in (start, end] also satisfies the inequality
  because the array is sorted, so add (end - start) to the count and
  advance start. Otherwise shrink end. O(n^2) overall.
"""


class Solution:
    def searchTriplets(self, arr, target):
        count = 0
        arr.sort()
        for i, n in enumerate(arr):
            start_idx = i + 1
            end_idx = len(arr) - 1
            while start_idx < end_idx:
                if n + arr[start_idx] + arr[end_idx] < target:
                    count += end_idx - start_idx
                    start_idx += 1
                else:
                    end_idx -= 1

        return count


if __name__ == "__main__":
    s = Solution()

    assert s.searchTriplets([-2, 0, 1, 3], 2) == 2     # Example 1
    assert s.searchTriplets([], 0) == 0                # Example 2
    assert s.searchTriplets([0], 0) == 0               # Example 3

    print("triplets_with_smaller_sum.py: all tests passed")
