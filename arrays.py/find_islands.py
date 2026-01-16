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