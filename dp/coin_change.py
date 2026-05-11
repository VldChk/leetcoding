"""
LeetCode 322 - Coin Change (Medium)
https://leetcode.com/problems/coin-change/

You are given an integer array coins representing coins of different
denominations and an integer amount representing a total amount of
money.

Return the fewest number of coins that you need to make up that amount.
If that amount of money cannot be made up by any combination of the
coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Solution idea:
  Unbounded-coin DP. dp[i] = fewest coins to form amount i. Seed dp[0]
  = 0 and dp[c] = 1 for c in coins. For each coin, sweep
  i = coin..amount and set dp[i] = min(dp[i], dp[i - coin] + 1). The
  outer loop over coins (instead of inner) keeps the algorithm
  unbounded (each coin can be reused). Return dp[amount], or -1 if it
  is still infinity.
"""
from typing import List, Union
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int | float:
        if amount == 0:
            return 0
        dp: List[Union[int, float]] = [float('inf') if i not in coins else 1 for i in range(amount+1)]
        dp[0] = 0
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] = min(dp[i], dp[i-coin] + 1)
        return dp[-1] if dp[-1] != float('inf') else -1


if __name__ == "__main__":
    s = Solution()

    assert s.coinChange([1, 2, 5], 11) == 3      # Example 1: 5+5+1
    assert s.coinChange([2], 3) == -1            # Example 2: impossible
    assert s.coinChange([1], 0) == 0             # Example 3: zero coins

    print("coin_change.py: all tests passed")
