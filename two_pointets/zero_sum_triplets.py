"""
LeetCode 15 - 3Sum (Medium)
https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j],
nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] +
nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

This file holds two implementations:
  1. The standalone `searchTriplets(arr)` is an O(n^3) brute-force
     reference (Grokking-style) that exhaustively enumerates index
     triples and dedupes via a tuple-of-sorted-values set. Returns a
     list of triplets summing to 0; useful for cross-checking.
  2. `Solution.threeSum(self, nums)` is the canonical LC 15 entry point
     using sort + fixed-element + two-pointer scan with duplicate skip.

The LC submission uses (2); (1) is kept as a brute-force oracle.

Solution idea (Solution.threeSum):
  Identical to the sibling `3s.py`: sort, fix nums[i] (skipping equal
  duplicates), and look for pairs in the suffix that sum to -nums[i]
  using two pointers from both ends. A set absorbs same-value triplet
  duplicates that the duplicate-skip cannot prevent in pathological
  inputs.
"""


def searchTriplets(arr):
    # bruteforce
    d = {
        tuple(sorted([arr[i], arr[j], arr[k]]))
        for i in range(len(arr))
        for j in range(len(arr))
        for k in range(len(arr))
        if i != j and i != k and k != j and arr[i] + arr[j] + arr[k] == 0
    }
    # print(d)
    triplets = [list(t) for t in d]
    return triplets



class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        nums.sort()
        triplets = set()
        # print(arr)

        for i, n in enumerate(nums):
            if i > 0 and n == nums[i-1]:
                continue
            # print(f"start for {n}")
            start_idx = i+1
            end_idx = len(nums) - 1
            target_sum = (-1) * n
            while start_idx < end_idx:
                if nums[start_idx] + nums[end_idx] > target_sum:
                    end_idx -= 1
                elif nums[start_idx] + nums[end_idx] < target_sum:
                    start_idx += 1
                else:
                    # print("Found", [arr[start_idx], arr[end_idx], n])
                    t = (n, nums[start_idx], nums[end_idx])
                    triplets.add(t)
                    start_idx += 1
                    end_idx -= 1
        return [list(t) for t in triplets]


if __name__ == "__main__":
    s = Solution()

    def normalize(triplets):
        return sorted(sorted(t) for t in triplets)

    # Example 1
    assert normalize(s.threeSum([-1, 0, 1, 2, -1, -4])) == \
        normalize([[-1, -1, 2], [-1, 0, 1]])
    # Example 2
    assert normalize(s.threeSum([0, 1, 1])) == []
    # Example 3
    assert normalize(s.threeSum([0, 0, 0])) == \
        normalize([[0, 0, 0]])

    # Cross-check: brute-force oracle agrees on Example 1.
    assert normalize(searchTriplets([-1, 0, 1, 2, -1, -4])) == \
        normalize([[-1, -1, 2], [-1, 0, 1]])

    print("zero_sum_triplets.py: all tests passed")
