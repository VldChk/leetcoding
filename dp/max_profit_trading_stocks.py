"""
LeetCode 2291 - Maximum Profit From Trading Stocks (Medium, Premium)
https://leetcode.com/problems/maximum-profit-from-trading-stocks/

You are given two 0-indexed integer arrays of the same length present
and future where present[i] is the current price of the i-th stock and
future[i] is the price of the i-th stock a year in the future. You may
buy each stock at most once. You are also given an integer budget
representing the amount of money you currently have.

Return the maximum amount of profit you can make.

Solution idea:
  Classic 0/1 knapsack. Pre-filter to stocks with strictly positive
  profit (future - present > 0) that also fit individually under the
  budget. Then dp[cash] = max profit achievable using exactly `cash`
  budget. Iterate stocks; for each, walk cash from budget down to
  price (descending, to ensure 0/1 not unbounded usage) and update
  dp[cash] = max(dp[cash], dp[cash - price] + profit). Return dp[budget].
"""
from typing import List
class Solution:
    def maximumProfit(self, present: List[int], future: List[int], budget: int) -> int:
        f: List[int] = []
        p: List[int] = []
        for i in range(len(present)):
            if future[i] - present[i] > 0 and present[i] <= budget:
                f.append(future[i] - present[i])
                p.append(present[i])
        if len(f) == 0:
            return 0
        elif len(f) == 1:
            return f[0]

        dp: List[int] = [0 for _ in range(budget+1)]

        for price, profit in zip(p, f):
            for cash in range(budget, price-1, -1):
                dp[cash] = max(dp[cash], dp[cash-price] + profit)

        return dp[-1]


if __name__ == "__main__":
    s = Solution()

    assert s.maximumProfit([5, 4, 6, 2, 3], [8, 5, 4, 3, 5], 10) == 6   # Example 1
    assert s.maximumProfit([2, 2, 5], [3, 4, 10], 6) == 5               # Example 2
    assert s.maximumProfit([3, 3, 12], [0, 3, 15], 10) == 0             # Example 3

    print("max_profit_trading_stocks.py: all tests passed")
