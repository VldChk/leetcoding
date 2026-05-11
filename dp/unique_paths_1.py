"""
LeetCode 62 - Unique Paths (Medium)
https://leetcode.com/problems/unique-paths/

There is a robot on an m x n grid. The robot is initially located at
the top-left corner (i.e., grid[0][0]). The robot tries to move to the
bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only
move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique
paths that the robot can take to reach the bottom-right corner.

Solution idea:
  1-D DP rolling along rows. dp[j] holds the number of paths to column
  j of the *current* row. Each row update sets dp[j] += dp[j-1] (paths
  ending here equal paths from above + paths from the left). Sentinel
  dp[0] = 0, dp[1] = 1 initially so the first row becomes all-1s and
  subsequent rows accumulate correctly. O(mn) time, O(n) space.
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [0] * (n+1)
        dp[1] = 1
        for _ in range(m):
            for j in range(1, n+1):
                prev_j = j-1
                dp[j] = dp[prev_j] + dp[j]
        return dp[-1]


if __name__ == "__main__":
    s = Solution()

    assert s.uniquePaths(3, 7) == 28    # Example 1
    assert s.uniquePaths(3, 2) == 3     # Example 2

    print("unique_paths_1.py: all tests passed")
        