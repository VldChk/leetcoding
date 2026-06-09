"""
LeetCode 289 — Game of Life (Medium)
https://leetcode.com/problems/game-of-life/

Given an m x n `board` of live (1) / dead (0) cells, compute the next state
according to Conway's rules and write it back IN PLACE:
    1. A live cell with <2 live neighbours dies (under-population).
    2. A live cell with 2 or 3 live neighbours survives.
    3. A live cell with >3 live neighbours dies (over-population).
    4. A dead cell with exactly 3 live neighbours becomes live (reproduction).
Diagonals count as neighbours; cells outside the grid are treated as dead.

Examples:
    [[0,1,0],[0,0,1],[1,1,1],[0,0,0]]
    -> [[0,0,0],[1,0,1],[0,1,1],[0,1,0]]

    [[1,1],[1,0]]
    -> [[1,1],[1,1]]

Idea — snapshot neighbours first, then update:
The naive in-place mutation would let already-updated cells contaminate the
neighbour counts of their successors. This solution first builds a `tmp`
array holding each cell's neighbour list (snapshot), then walks the board a
second time and applies the four rules using the snapshot. Two passes, O(mn)
extra space — simple and clearly correct.

Note on indexing: this solution uses `board[j][i]` with `j` for row and `i`
for column. Slicing (`board[j-1][max(i-1, 0):i+2]`) naturally clips at the
left/right edges; the `if j == 0` / `if j == len(board)-1` guards handle the
top/bottom edges.

Complexity:
    Time  O(m*n) — two passes, neighbour lookup is constant size
    Space O(m*n) for the snapshot `tmp`
"""
from typing import List

class Solution:
    def gameOfLife(self, board: List[List[int]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        def _get_neigbours(i: int, j: int) -> List[int]:
            res = []
            # upper row
            upper_row = [] if j == 0 else board[j-1][max(i-1, 0):i+2]
            res.extend(upper_row)
            # lower_row
            lower_row = [] if j == len(board)-1 else board[j+1][max(i-1, 0):i+2]
            res.extend(lower_row)
            # left
            left = [] if i == 0 else [board[j][i-1]]
            res.extend(left)

            # right
            right = [] if i == len(board[j])-1 else [board[j][i+1]]
            res.extend(right)
            return res
        tmp = []

        for j in range(len(board)):
            row = []
            for i in range(len(board[j])):
                n = _get_neigbours(i, j)
                row.append(n)
            tmp.append(row)

        for j in range(len(board)):
            for i in range(len(board[j])):
                n = tmp[j][i]
                if sum(n) < 2 and board[j][i] == 1:
                    board[j][i] = 0
                elif sum(n) in [2,3] and board[j][i] == 1:
                    board[j][i] = 1
                elif sum(n) > 3  and board[j][i] == 1:
                    board[j][i] = 0
                elif sum(n) == 3 and board[j][i] == 0:
                    board[j][i] = 1
                else:
                    board[j][i] = 0


if __name__ == "__main__":
    sol = Solution()

    # Example 1 (official LC sample)
    board = [[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]]
    sol.gameOfLife(board)
    assert board == [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]], board

    # Example 2 (official LC sample)
    board = [[1, 1], [1, 0]]
    sol.gameOfLife(board)
    assert board == [[1, 1], [1, 1]], board

    # Single live cell — dies of under-population
    board = [[1]]
    sol.gameOfLife(board)
    assert board == [[0]], board

    # All dead stays all dead
    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    sol.gameOfLife(board)
    assert board == [[0, 0, 0], [0, 0, 0], [0, 0, 0]], board

    # Blinker oscillator — vertical bar -> horizontal bar
    board = [[0, 1, 0], [0, 1, 0], [0, 1, 0]]
    sol.gameOfLife(board)
    assert board == [[0, 0, 0], [1, 1, 1], [0, 0, 0]], board

    print("game_of_life.py: all tests passed")
