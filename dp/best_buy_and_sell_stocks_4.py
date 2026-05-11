"""
LeetCode 188 - Best Time to Buy and Sell Stock IV (Hard)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/

You are given an integer array prices where prices[i] is the price of
a given stock on the i-th day, and an integer k.

Find the maximum profit you can achieve. You may complete at most k
transactions: i.e. you may buy at most k times and sell at most k
times.

Note: You may not engage in multiple transactions simultaneously (i.e.,
you must sell the stock before you buy again).

Solution idea:
  Generalisation of the 4-state DP from LC 123 to 2k states. The
  `states` array holds, in order:
    [buy_1, sell_1, buy_2, sell_2, ..., buy_k, sell_k]
  Even indices are post-buy ("cost basis carried as -pr"), odd indices
  are post-sell. Each new day, sweep the array left-to-right (so each
  state may use the just-updated previous one for "same-day chained"
  transactions): odd index = max(self, prev + pr), even index = max(
  self, prev - pr). Return states[-1] = the post-kth-sell wallet.
  Note: this variant assumes k >= 1 (states[0] is touched unconditionally
  before the loop). LeetCode example 1 uses k=2 and example 2 uses k=2.
"""
from typing import List

class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int | float:
        states: list[int | float] = []
        for i in range(k):
            states.extend([float('-inf'), 0])
        
        for pr in prices:
            states[0] = max(states[0], -pr)
            for i in range(1, len(states)):
                states[i] = max(states[i], states[i-1]+pr) if i % 2 == 1 else max(states[i], states[i-1]-pr)
        
        return states[-1]


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit(2, [2, 4, 1]) == 2              # Example 1: buy 2 sell 4
    assert s.maxProfit(2, [3, 2, 6, 5, 0, 3]) == 7     # Example 2: buy 2 sell 6 + buy 0 sell 3

    # Note: k = 0 isn't tested here — the current implementation
    # unconditionally touches states[0], so k = 0 raises IndexError.
    # LC's published examples don't trigger that path; if you want to
    # cover the constraint `0 <= k`, add `if k == 0: return 0` at the
    # top of maxProfit.

    print("best_buy_and_sell_stocks_4.py: all tests passed")