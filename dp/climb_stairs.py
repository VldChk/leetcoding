"""
LeetCode 70 - Climbing Stairs (Easy)
https://leetcode.com/problems/climbing-stairs/

You are climbing a staircase. It takes n steps to reach the top.

Each time you can either climb 1 or 2 steps. In how many distinct ways
can you climb to the top?

Solution idea:
  This is the Fibonacci recurrence with offset: ways(n) = ways(n-1) +
  ways(n-2), because the last move is either +1 (from n-1) or +2
  (from n-2). Tabulate bottom-up. O(n) time, O(n) space (trivially
  reducible to O(1) by rolling two variables, but LC accepts either).
"""


class Solution:
    def climbStairs(self, n: int) -> int:
        if n < 2:
            return 1
        elif n < 3:
            return 2
        dp = [0] * (n+1)
        dp[0] = 1
        dp[1] = 1
        for i in range(2, n+1):
            dp[i] = dp[i-1] + dp[i-2]
        return dp[-1]


if __name__ == "__main__":
    s = Solution()

    assert s.climbStairs(2) == 2     # Example 1: 1+1 or 2
    assert s.climbStairs(3) == 3     # Example 2: 1+1+1, 1+2, 2+1

    print("climb_stairs.py: all tests passed")
