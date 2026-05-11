"""
LeetCode 309 - Best Time to Buy and Sell Stock with Cooldown (Medium)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/

You are given an array prices where prices[i] is the price of a given
stock on the i-th day.

Find the maximum profit you can achieve. You may complete as many
transactions as you like (i.e., buy one and sell one share of the
stock multiple times) with the following restrictions:

  - After you sell your stock, you cannot buy stock on the next day
    (i.e., cooldown one day).

Note: You may not engage in multiple transactions simultaneously (i.e.,
you must sell the stock before you buy again).

Solution idea:
  Top-down DP with memoization on (index, buying_flag). At each index
  you can always "rest" -> dfs(idx+1, buying). If buying is True, you
  may buy -> dfs(idx+1, False) - prices[idx]. If buying is False, you
  may sell -> dfs(idx+2, True) + prices[idx] (idx+2 enforces the
  one-day cooldown). Memo collapses the exponential branching to O(n).
"""
from typing import List
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        d: dict[tuple[int, bool], int] = {}
        def dfs(idx: int, buying: bool) -> int:
            if idx >= len(prices):
                return 0
            if (idx, buying) in d:
                return d[(idx, buying)]
            
            cooldown = dfs(idx+1, buying)

            if buying:
                buy = dfs(idx+1, not buying) - prices[idx]
                d[(idx, buying)] = max(buy, cooldown)
            else:
                sell = dfs(idx+2, not buying) + prices[idx]
                d[(idx, buying)] = max(sell, cooldown)
            
            return d[(idx, buying)]
        
        return dfs(0, True)


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([1, 2, 3, 0, 2]) == 3     # Example 1: buy 1 sell 2, cooldown, buy 0 sell 2
    assert s.maxProfit([1]) == 0                 # Example 2

    print("best_buy_sell_stocks_cooldown.py: all tests passed")