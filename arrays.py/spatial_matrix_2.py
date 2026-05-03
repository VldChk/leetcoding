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