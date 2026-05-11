"""
LeetCode 119 - Pascal's Triangle II (Easy)
https://leetcode.com/problems/pascals-triangle-ii/

Given an integer rowIndex, return the rowIndex-th (0-indexed) row of
the Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers
directly above it.

Solution idea:
  Each entry on row i is the binomial coefficient C(i, j). `math.comb`
  computes it directly, so the whole row is one comprehension. The
  follow-up asks for O(rowIndex) extra space; `math.comb` allocates a
  small int per call so the technical answer is "yes, asymptotically."
"""
import math
from typing import List
class Solution:
    def getRow(self, rowIndex: int) -> List[int]:
        return [math.comb(rowIndex, i) for i in range(rowIndex+1)]


if __name__ == "__main__":
    s = Solution()

    assert s.getRow(3) == [1, 3, 3, 1]      # Example 1
    assert s.getRow(0) == [1]               # Example 2
    assert s.getRow(1) == [1, 1]            # Example 3

    print("pascal_triangle_2.py: all tests passed")
