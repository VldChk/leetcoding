"""
LeetCode 123 - Best Time to Buy and Sell Stock III (Hard)
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/

You are given an array prices where prices[i] is the price of a given
stock on the i-th day.

Find the maximum profit you can achieve. You may complete at most two
transactions.

Note: You may not engage in multiple transactions simultaneously (i.e.,
you must sell the stock before you buy again).

Solution idea:
  Four rolling state machine. At every day, track the best-so-far of
  four "wallet states":
    buy_first_time   = best profit after the first buy   (so cost basis
                       baked in as -pr)
    sell_first_time  = best profit after the first sell
    buy_second_time  = best profit after the second buy
    sell_second_time = best profit after the second sell
  Each is updated as `max(previous, transition_from_prior_state)`. The
  order of the four updates within a single day matters — each later
  state may legally use the *just-updated* earlier state, which encodes
  "you may buy and sell on the same day to start the next leg." O(n)
  time, O(1) space.
"""
from typing import List
class Solution:
    def maxProfit(self, prices: List[int]) -> int | float:
        buy_first_time = float('-inf')
        sell_first_time = 0
        buy_second_time = float('-inf')
        sell_second_time = 0

        for pr in prices:
            buy_first_time = max(buy_first_time, -pr)
            sell_first_time = max(sell_first_time, buy_first_time+pr)
            buy_second_time = max(buy_second_time, sell_first_time-pr)
            sell_second_time = max(sell_second_time, buy_second_time+pr)
        
        return sell_second_time


if __name__ == "__main__":
    s = Solution()

    assert s.maxProfit([3, 3, 5, 0, 0, 3, 1, 4]) == 6    # Example 1: buy 0 sell 3, buy 1 sell 4
    assert s.maxProfit([1, 2, 3, 4, 5]) == 4             # Example 2: single transaction
    assert s.maxProfit([7, 6, 4, 3, 1]) == 0             # Example 3: monotone decline

    print("best_buy_and_sell_stocks_3.py: all tests passed")