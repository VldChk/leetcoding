"""
LeetCode 16 - 3Sum Closest (Medium)
https://leetcode.com/problems/3sum-closest/

Given an integer array nums of length n and an integer target, find
three integers in nums such that the sum is closest to target.

Return the sum of the three integers.

You may assume that each input would have exactly one solution.

Note: this file uses the Grokking-style name `searchTriplet(arr,
target_sum)` rather than LeetCode's `threeSumClosest(self, nums,
target)`. The algorithm is identical; only the method label differs.
The tests below call the method as written here.

Solution idea:
  Sort. Fix the leftmost element n at i (skipping equal duplicates),
  then run two pointers (start, end) inward. At each step compute the
  triplet sum and update closest_sum if it's closer than the running
  best (tie-break to the smaller sum). Move the pointer toward the
  target side; on exact hit return target immediately.
"""


class Solution:
    def searchTriplet(self, arr, target_sum):
        arr.sort()
        closest_dist = 2**31 - 1
        closest_sum = 2**31 - 1

        for i, n in enumerate(arr):
            if i > 0 and n == arr[i - 1]:
                continue
            start_idx = i + 1
            end_idx = len(arr) - 1
            while start_idx < end_idx:
                it = n + arr[start_idx] + arr[end_idx]
                if abs(it - target_sum) <= closest_dist:
                    if abs(it - target_sum) == closest_dist:
                        closest_sum = min(closest_sum, it)
                    else:
                        closest_sum = it
                    closest_dist = abs(it - target_sum)
                if it > target_sum:
                    end_idx -= 1
                elif it < target_sum:
                    start_idx += 1
                else:
                    return target_sum
        return closest_sum


if __name__ == "__main__":
    s = Solution()

    assert s.searchTriplet([-1, 2, 1, -4], 1) == 2     # Example 1
    assert s.searchTriplet([0, 0, 0], 1) == 0          # Example 2

    print("closest_triplet_sum.py: all tests passed")
