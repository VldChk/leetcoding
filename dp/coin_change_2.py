"""
LeetCode 518 - Coin Change II (Medium)
https://leetcode.com/problems/coin-change-ii/

You are given an integer array coins representing coins of different
denominations and an integer amount representing a total amount of
money.

Return the number of combinations that make up that amount. If that
amount of money cannot be made up by any combination of the coins,
return 0.

You may assume that you have an infinite number of each kind of coin.

The answer is guaranteed to fit into a signed 32-bit integer.

Solution idea:
  Unbounded knapsack count. dp[i] = number of combinations that form
  amount i. Initialize dp[0] = 1 (one way to make 0: use nothing).
  For each coin, sweep i = coin..amount and add dp[i - coin] into
  dp[i]. The KEY is the outer loop being over coins (not amounts) —
  that prevents counting permutations as distinct combinations.
"""
from typing import List
class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        res = [0 for _ in range(amount+1)]
        res[0] = 1
        for coin in coins:
            for i in range(coin, amount+1):
                res[i] = res[i-coin] + res[i]
        return res[-1]


if __name__ == "__main__":
    s = Solution()

    assert s.change(5, [1, 2, 5]) == 4       # Example 1
    assert s.change(3, [2]) == 0             # Example 2
    assert s.change(10, [10]) == 1           # Example 3

    print("coin_change_2.py: all tests passed")
