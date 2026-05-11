"""
LeetCode 2951 - Find the Peaks (Easy)
https://leetcode.com/problems/find-the-peaks/

You are given a 0-indexed array `mountain`. Your task is to find all
the peaks in the `mountain` array.

Return an array that consists of indices of peaks in the given array
in any order.

Notes:
  - A peak is defined as an element that is strictly greater than its
    neighboring elements.
  - The first and last elements of the array are not a peak.

Solution idea:
  Plain linear scan over the interior indices [1, n-2]. An index i is
  a peak iff mountain[i] is strictly greater than both mountain[i-1]
  and mountain[i+1]. Return collected indices in increasing order.
  O(n) time, O(1) auxiliary space.
"""
from typing import List
class Solution:
    def findPeaks(self, mountain: List[int]) -> List[int]:
        res: List[int] = []
        if len(mountain) < 3:
            return res
        
        for i in range(1, len(mountain)-1):
            if mountain[i] > mountain[i+1] and mountain[i] > mountain[i-1]:
                res.append(i)

        return res


if __name__ == "__main__":
    s = Solution()

    # LC accepts indices in any order; sort for comparison.
    assert sorted(s.findPeaks([2, 4, 4])) == []                # Example 1
    assert sorted(s.findPeaks([1, 4, 3, 8, 5])) == [1, 3]      # Example 2

    print("find_peaks.py: all tests passed")
