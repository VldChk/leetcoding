"""
LeetCode 1605 - Find Valid Matrix Given Row and Column Sums (Medium)
https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/

You are given two arrays rowSum and colSum of non-negative integers
where rowSum[i] is the sum of the elements in the i-th row and
colSum[j] is the sum of the elements of the j-th column of a 2D matrix.
The dimensions of the matrix are rowSum.length x colSum.length.

Find any matrix of non-negative integers of size
rowSum.length x colSum.length that satisfies the rowSum and colSum
requirements. Return any such matrix. The test cases are generated so
that there exists at least one valid matrix.

Solution idea:
  Greedy "northwest corner" rule. Walk a single (i, j) pointer through
  the grid: at each cell, place min(rowSum[i], colSum[j]) — the most
  this cell can absorb without overshooting either sum. Subtract from
  both. Whichever runs out, advance that dimension; the other one keeps
  its remaining budget. The matrix's other cells stay 0. O(m + n)
  non-zero cells, O(m*n) total to fill the rest with zeros.
"""
from typing import List
class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        matrix = [[0] * len(colSum) for _ in range(len(rowSum))]
        i = 0
        j = 0
        while i < len(rowSum) and j < len(colSum):
            matrix[i][j] = min(rowSum[i], colSum[j])
            rowSum[i] -= matrix[i][j]
            colSum[j] -= matrix[i][j]
            if rowSum[i] == 0:
                i+=1
            else:
                j+=1
        return matrix


if __name__ == "__main__":
    s = Solution()

    def check(rowSum: list[int], colSum: list[int]) -> None:
        # validate the returned matrix matches the requested row/col sums
        r_in = rowSum[:]
        c_in = colSum[:]
        m = s.restoreMatrix(rowSum, colSum)
        assert len(m) == len(r_in) and all(len(row) == len(c_in) for row in m)
        assert all(v >= 0 for row in m for v in row)
        assert [sum(row) for row in m] == r_in
        assert [sum(m[i][j] for i in range(len(r_in))) for j in range(len(c_in))] == c_in

    check([3, 8], [4, 7])                         # Example 1
    check([5, 7, 10], [8, 6, 8])                   # Example 2

    print("reconstruct_matrix.py: all tests passed")
