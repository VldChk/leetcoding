"""
LeetCode 1711 - Count Good Meals (Medium)
https://leetcode.com/problems/count-good-meals/

A good meal is a meal that contains exactly two different food items
with a sum of deliciousness equal to a power of two.

You can pick any two different foods to make a good meal.

Given an array of integers deliciousness where deliciousness[i] is the
deliciousness of the i-th food item, return the number of different
good meals you can make from this list modulo 10^9 + 7.

Note: indices i and j with i != j are considered different even if
deliciousness[i] == deliciousness[j].

Solution idea:
  Bound the candidate "powers of two" by 2*min .. 2*max so we only
  consider sums achievable from two array values. Count occurrences in
  a dict d. For each (k, v) and each power-of-two t, the matching
  partner is (t - k); guard against double-counting by requiring
  (t - k) >= k. When k == t-k, pairs come from C(v, 2). Otherwise the
  contribution is v * d[t - k]. Reduce the answer modulo 1e9 + 7 at the
  end.
"""
from typing import List
class Solution:
    def countPairs(self, deliciousness: List[int]) -> int:
        deliciousness.sort()
        twos = [2**i for i in range(0, 22) if 2**i >= min(deliciousness) * 2 and 2**i <= max(deliciousness) * 2]
        d: dict[int, int] = {}
        for n in deliciousness:
            d[n] = d.get(n, 0) + 1
        res = 0
        for k, v in d.items():
            for t in twos:
                if (t-k) < k:
                    continue
                if k == t-k:
                    res += v * (v - 1) // 2
                elif t - k in d:
                    res += (v * d[t - k])

        return res % (10**9 + 7)


if __name__ == "__main__":
    s = Solution()

    assert s.countPairs([1, 3, 5, 7, 9]) == 4              # Example 1
    assert s.countPairs([1, 1, 1, 3, 3, 3, 7]) == 15       # Example 2

    print("good_meal_count.py: all tests passed")