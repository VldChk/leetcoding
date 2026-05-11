"""
LeetCode 1679 - Max Number of K-Sum Pairs (Medium)
https://leetcode.com/problems/max-number-of-k-sum-pairs/

You are given an integer array nums and an integer k.

In one operation, you can pick two numbers from the array whose sum
equals k and remove them from the array.

Return the maximum number of operations you can perform on the array.

Solution idea:
  Hash-map of remaining counts. For each n in nums, look up complement
  (k - n). If it's currently available, pair off (one operation, remove
  one occurrence of the complement). Otherwise stash n for later. This
  is O(n) and avoids the need for sorting.
"""
from typing import List
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        d: dict[int, int] = {}
        res = 0
        for n in nums:
            t = k - n
            if t in d:
                res += 1
                if d[t] == 1:
                    del d[t]
                else:
                    d[t] -= 1
            else:
                d[n] = d.get(n, 0) + 1
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.maxOperations([1, 2, 3, 4], 5) == 2           # Example 1
    assert s.maxOperations([3, 1, 3, 4, 3], 6) == 1        # Example 2

    print("k_sum_pairs.py: all tests passed")