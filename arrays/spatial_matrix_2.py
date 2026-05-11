"""
LeetCode 59 - Spiral Matrix II (Medium)
https://leetcode.com/problems/spiral-matrix-ii/

(Filename "spatial_matrix_2" is a typo for "spiral_matrix_2".)

Given a positive integer n, generate an n x n matrix filled with the
elements from 1 to n^2 in spiral order.

Solution idea:
  Maintain four boundary pointers (up, down, left, right) shrinking
  inward each loop iteration. In each ring: walk top edge L->R, right
  edge T->B, bottom edge R->L (only if up != down), left edge B->T
  (only if left != right), incrementing a running counter `cnt` written
  into each visited cell. The matrix is preallocated to all-1 and `cnt`
  is added (so cell receives `cnt + 1`). Loop ends when cnt reaches n^2.
"""
from typing import List
class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        row = [1] * n
        matrix: List[List[int]] = []
        for i in range(n):
            r = row.copy()
            matrix.append(r)

        up = left = 0
        down = right = n - 1

        cnt = 0

        while cnt < n**2:
            for i in range(left, right+1):
                matrix[up][i] += cnt
                cnt += 1
            
            for i in range(up + 1, down + 1):
                matrix[i][right] += cnt
                cnt += 1
            
            if up != down:
                for i in range(right - 1, left - 1, -1):
                    matrix[down][i] += cnt
                    cnt += 1
            
            if left != right:
                for i in range(down - 1, up, -1):
                    matrix[i][left] += cnt
                    cnt += 1
            
            left += 1
            right -= 1
            up += 1
            down -= 1
        return matrix


if __name__ == "__main__":
    s = Solution()

    assert s.generateMatrix(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]]   # Example 1
    assert s.generateMatrix(1) == [[1]]                               # Example 2

    print("spatial_matrix_2.py: all tests passed")