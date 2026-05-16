"""
LeetCode 875 - Koko Eating Bananas (Medium)
https://leetcode.com/problems/koko-eating-bananas/

Koko loves to eat bananas. There are n piles of bananas, the i-th pile
has piles[i] bananas. The guards have gone and will come back in h
hours.

Koko can decide her bananas-per-hour eating speed of k. Each hour she
chooses some pile of bananas and eats k bananas from that pile. If the
pile has less than k bananas, she eats all of them instead and will
not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the
bananas before the guards return. Return the minimum integer k such
that she can eat all the bananas within h hours.

Solution idea:
  Binary search on the answer. The candidate space is [1, max(piles)]:
  k = max(piles) always works (one pile per hour) and k = 0 is invalid.
  For a given k, hours spent = sum(ceil(p/k) for p in piles), computed
  as `(p-1)//k + 1` to avoid float math. Predicate "hours <= h" is
  monotone non-increasing in k, so binary search for the smallest k
  with hours(k) <= h. O(n log max(piles)).
"""
from typing import List
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        start_idx = 1
        end_idx = max(piles)

        while start_idx <= end_idx:
            if start_idx == end_idx:
                return start_idx
            else:
                mid_idx = (start_idx + end_idx) // 2
                hrs = sum(((p - 1)//mid_idx + 1) for p in piles)
                if hrs > h:
                    start_idx = mid_idx + 1
                else:
                    end_idx = mid_idx
        return -1



if __name__ == "__main__":
    s = Solution()

    assert s.minEatingSpeed([3, 6, 7, 11], 8) == 4              # Example 1
    assert s.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30        # Example 2
    assert s.minEatingSpeed([30, 11, 23, 4, 20], 6) == 23        # Example 3

    print("koko_eats_bananas.py: all tests passed")
