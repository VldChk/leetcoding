"""
LeetCode 118 - Pascal's Triangle (Easy)
https://leetcode.com/problems/pascals-triangle/

Given an integer numRows, return the first numRows of Pascal's
triangle.

In Pascal's triangle, each number is the sum of the two numbers
directly above it.

Solution idea:
  Skip the "add previous two" recurrence entirely and just compute each
  row directly from binomial coefficients: row i is [C(i, 0), C(i, 1),
  ..., C(i, i)]. `math.comb` runs in O(min(j, i-j)); the whole table is
  O(numRows^2) just like the additive form, but the code is one line
  per row.
"""
import math
from typing import List
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        if numRows == 0:
            return [[1]]
        res = [[1]]
        for i in range(1, numRows):
            t = [math.comb(i, j) for j in range(i+1)]
            res.append(t)
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.generate(5) == [
        [1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1],
    ]                                                        # Example 1
    assert s.generate(1) == [[1]]                            # Example 2

    print("pascal_triangle.py: all tests passed")