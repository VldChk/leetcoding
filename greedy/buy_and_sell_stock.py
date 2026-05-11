"""
LeetCode 121 - Best Time to Buy and Sell Stock (Easy)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/

You are given an array prices where prices[i] is the price of a given
stock on the i-th day.

You want to maximize your profit by choosing a single day to buy one
stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If
you cannot achieve any profit, return 0.

Solution idea:
  Single pass tracking the minimum price seen so far. At each step the
  best profit ending today is prices[i] - running_min; take the max of
  that against the running best. Updating min after computing the
  profit ensures buy-day strictly precedes sell-day. O(n) time, O(1)
  space.
"""
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) < 2:
             return 0
        min_price = prices[0]
        profit = 0
        for i in range(1, len(prices)):
            profit = max(profit, (prices[i] - min_price))
            min_price = min(min_price, prices[i])
        return profit


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 5     # Example 1: buy@1, sell@6
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0        # Example 2: monotone decline

    print("buy_and_sell_stock.py: all tests passed")