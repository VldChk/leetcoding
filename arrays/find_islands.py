"""
LeetCode 200 - Number of Islands (Medium)
https://leetcode.com/problems/number-of-islands/

Given an m x n 2D binary grid which represents a map of '1's (land) and
'0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent
lands horizontally or vertically. You may assume all four edges of the
grid are surrounded by water.

Solution idea:
  Scan every cell. When an unvisited '1' is hit, increment the island
  counter and DFS-flood all 4-connected '1' cells, recording them in a
  visited set so the outer scan never starts a new island from them.
"""
from typing import List
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def process_point(current_pos_i, current_pos_j, memory, m, n):
            def _check_and_add(pos, memory, m, n):
                x, y = pos
                if pos not in memory and grid[y][x] == '1':
                    memory.add(pos)
                    process_point(x, y, memory, m, n)
            left = max(0, current_pos_i-1)
            right = min(m, current_pos_i+1)
            top = max(0, current_pos_j-1)
            bottom = min(n, current_pos_j+1)
            _check_and_add((left, current_pos_j), memory,  m, n)
            _check_and_add((right, current_pos_j), memory,  m, n)
            _check_and_add((current_pos_i, top), memory,  m, n)
            _check_and_add((current_pos_i, bottom), memory,  m, n)
        
        n = len(grid) -1
        m = len(grid[0]) -1
        memory = set()
        queue = []
        counter = 0
        for j, row in enumerate(grid):
            for i, cell in enumerate(row):
                if (i, j) not in memory and cell == '1':
                    counter += 1
                    memory.add((i, j))
                    process_point(i, j, memory, m, n)
        return counter


if __name__ == "__main__":
    s = Solution()

    # Example 1: one big L-shaped island.
    grid1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert s.numIslands(grid1) == 1

    # Example 2: three separate islands.
    grid2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert s.numIslands(grid2) == 3

    print("find_islands.py: all tests passed")