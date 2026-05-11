"""
LeetCode 122 - Best Time to Buy and Sell Stock II (Medium)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/

You are given an integer array prices where prices[i] is the price of
a given stock on the i-th day.

On each day, you may decide to buy and/or sell the stock. You can only
hold at most one share of the stock at any time. However, you can buy
it then immediately sell it on the same day.

Find and return the maximum profit you can achieve.

Solution idea (this implementation, valley-peak detection):
  Detect each "buy at a local valley, sell at the next local peak"
  pair by inspecting the local shape around each index:
    - i is a valley iff (i == 0 or prices[i-1] > prices[i]) AND
      i < n-1 AND prices[i+1] >= prices[i]: capture as the buy price.
    - i is a peak iff i > 0 AND prices[i-1] <= prices[i] AND
      (i == n-1 OR prices[i+1] < prices[i]): book profit
      (prices[i] - last buy).
  Strictly equivalent to the more common "sum of every up-step" trick
  but expressed in terms of explicit valleys and peaks. O(n) time.
"""
from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        profit = 0
        curr_stock_price = 0
        for i in range(len(prices)):
            if (i == 0 or prices[i-1] > prices[i]) and i < len(prices)-1 and prices[i+1] >= prices[i]:
                curr_stock_price = prices[i]
            elif i > 0 and prices[i-1] <= prices[i] and (i == len(prices)-1 or prices[i+1] < prices[i]):
                profit += (prices[i] - curr_stock_price)
        return profit


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([7, 1, 5, 3, 6, 4]) == 7     # Example 1: (5-1)+(6-3)
    assert s.maxProfit([1, 2, 3, 4, 5]) == 4        # Example 2: buy day 0, sell day 4
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0        # Example 3: never profitable

    print("buy_and_sell_stock_2.py: all tests passed")