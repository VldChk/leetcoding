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
        