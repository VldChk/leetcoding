"""
LeetCode 73 - Set Matrix Zeroes (Medium)
https://leetcode.com/problems/set-matrix-zeroes/

Given an m x n integer matrix, if an element is 0, set its entire row
and column to 0's. You must do it in place.

Solution idea:
  Two passes. First pass scans the matrix and records every row index
  and column index that contains a zero into two sets. Second pass
  rewrites: any row in the rows-set becomes all zeros; otherwise zero
  out only the columns in cols-set. Uses O(m + n) extra memory rather
  than the constant-space "use first row/col as markers" trick.
"""
from typing import List

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        rows: set[int] = set()
        cols: set[int] = set()
        for i, row in enumerate(matrix):
            for j, col in enumerate(row):
                if col == 0:
                    rows.add(i)
                    cols.add(j)
        for i, row in enumerate(matrix):
            if i in rows:
                matrix[i] = [0] * len(row)
            else:
                for j, col in enumerate(row):
                    if j in cols:
                        matrix[i][j] = 0


if __name__ == "__main__":
    s = Solution()

    # Example 1
    m1 = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    s.setZeroes(m1)
    assert m1 == [[1, 0, 1], [0, 0, 0], [1, 0, 1]]

    # Example 2
    m2 = [[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]]
    s.setZeroes(m2)
    assert m2 == [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]

    print("set_matrix_zeroes.py: all tests passed")