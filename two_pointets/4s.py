"""
LeetCode 18 - 4Sum (Medium)
https://leetcode.com/problems/4sum/

Given an array nums of n integers, return an array of all the unique
quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:
  - 0 <= a, b, c, d < n
  - a, b, c, and d are distinct.
  - nums[a] + nums[b] + nums[c] + nums[d] == target

You may return the answer in any order.

Solution idea:
  Sort. The outer loop fixes the first element with duplicate skipping;
  for each fixed value n, delegate to a 3Sum-style helper that searches
  the suffix for triplets summing to (target - n). The 3Sum helper
  itself is the standard fix-one + two-pointers pattern. Quadruplets
  are accumulated into a set to dedupe (handling same-value patterns
  that the duplicate-skip might miss).
"""


class Solution(object):
    def fourSum(self, nums, target):
        arr = nums
        def _find_triplets(arr, target, offset):
            triplets = []
            i = offset

            while i < len(arr) - 1:
                n = arr[i]
                if i > offset and n == arr[i-1]:
                    i += 1
                    continue
                start_idx = i + 1
                end_idx = len(arr) - 1
                while start_idx < end_idx:
                    it = n + arr[start_idx] + arr[end_idx]
                    if it - target > 0:
                        end_idx -= 1
                    elif it - target < 0:
                        start_idx += 1
                    else:
                        t = [n, arr[start_idx], arr[end_idx]]
                        triplets.append(t)
                        start_idx += 1
                        end_idx -= 1
                i += 1
            return triplets

        arr.sort()
        quadruplets = set()
        i = 0
        while i < len(arr) - 2:
            n = arr[i]
            if i > 0 and n == arr[i-1]:
                i += 1
                continue
            triplets = _find_triplets(arr, (-1) * (n - target), i + 1)
            for t in triplets:
                quadruplets.add(tuple([n] + t))
            i += 1
        return [list(q) for q in quadruplets]


if __name__ == "__main__":
    s = Solution()

    def normalize(quads):
        return sorted(sorted(q) for q in quads)

    assert normalize(s.fourSum([1, 0, -1, 0, -2, 2], 0)) == \
        normalize([[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]])  # Example 1
    assert normalize(s.fourSum([2, 2, 2, 2, 2], 8)) == \
        normalize([[2, 2, 2, 2]])                                   # Example 2

    print("4s.py: all tests passed")