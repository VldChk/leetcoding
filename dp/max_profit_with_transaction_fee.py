"""
LeetCode 714 - Best Time to Buy and Sell Stock with Transaction Fee (Medium)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/

You are given an array prices where prices[i] is the price of a given
stock on the i-th day, and an integer fee representing a transaction
fee.

Find the maximum profit you can achieve. You may complete as many
transactions as you like, but you need to pay the transaction fee for
each transaction.

Note: You may not engage in multiple transactions simultaneously (i.e.,
you must sell the stock before you buy again).

Solution idea:
  Two-state rolling DP. `buying` = best wallet state while currently
  holding a share (cost baked in as a negative number); `selling` =
  best wallet state while flat. Each day's transitions:
    buying'  = max(buying,  selling - pr)        # hold or open a new buy
    selling' = max(selling, buying + pr - fee)    # hold or close + pay fee
  The buying' uses the *old* selling (this day's update of buying may
  not consume this day's update of selling), so cache the old buying
  before overwriting it. O(n) time, O(1) space.
"""
from typing import List
class Solution:
    def maxProfit(self, prices: List[int], fee: int) -> int:

        buying = -prices[0]
        selling = 0

        for pr in prices:
            old_buy = buying
            buying = max(buying, selling-pr)
            selling = max(selling, old_buy + pr - fee)

        return selling


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([1, 3, 2, 8, 4, 9], 2) == 8           # Example 1
    assert s.maxProfit([1, 3, 7, 5, 10, 3], 3) == 6           # Example 2

    print("max_profit_with_transaction_fee.py: all tests passed")
