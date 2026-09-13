"""
LeetCode 64 - Minimum Path Sum (Medium)
https://leetcode.com/problems/minimum-path-sum/

Given an m x n grid of non-negative numbers, find a path from the top left
cell to the bottom right cell that minimises the sum of the numbers along
it. At every step you may only move down or right.

Example:
  grid = [[1, 3, 1],
          [1, 5, 1],
          [4, 2, 1]]   -> 7    (path 1 -> 3 -> 1 -> 1 -> 1)
  grid = [[1, 2, 3],
          [4, 5, 6]]   -> 12

Solution idea:
  Top-down DP with memoisation. The cheapest cost from a cell is its own
  value plus the cheaper of the costs from the cell to its right and the
  cell below; the bottom right cell costs just its own value, and a move
  off the grid is priced at a 2^31 - 1 sentinel so it is never chosen.
  Note that `i` indexes columns and `j` rows. O(m * n) time and space; the
  recursion is at most m + n <= 400 frames deep, under Python's default
  limit.
"""
from functools import cache
from typing import List


class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        n = len(grid[0])
        m = len(grid)

        @cache
        def solve(i: int, j: int) -> int:
            if i == n-1 and j == m-1:
                return grid[j][i]

            right = 2**31-1
            if i < n-1:
                right = solve(i+1, j)

            down = 2**31-1
            if j < m-1:
                down = solve(i, j+1)

            return min(grid[j][i] + right, grid[j][i] + down)

        return solve(0, 0)


if __name__ == "__main__":
    s = Solution()

    # Official examples
    assert s.minPathSum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7
    assert s.minPathSum([[1, 2, 3], [4, 5, 6]]) == 12

    print("minimal_path_sum.py: all tests passed")
