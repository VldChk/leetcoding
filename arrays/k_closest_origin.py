"""
LeetCode 973 - K Closest Points to Origin (Medium)
https://leetcode.com/problems/k-closest-points-to-origin/

Given an array of points where points[i] = [xi, yi] represents a point
on the X-Y plane and an integer k, return the k closest points to the
origin (0, 0).

The distance between two points on the X-Y plane is the Euclidean
distance (i.e., sqrt((x1 - x2)^2 + (y1 - y2)^2)).

You may return the answer in any order. The answer is guaranteed to be
unique (except for the order that it is in).

Solution idea:
  Compute Euclidean distance for each point, pair it with the point,
  sort by distance, and slice off the first k. The full sort is
  O(n log n) — a heap-based selection or quickselect would be faster
  (O(n log k) or O(n) avg), but LeetCode accepts the simpler version
  and the constants are small.
"""
import math
from typing import List
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        dist = [(math.sqrt(point[0]**2 + point[1]**2), point) for point in points]
        dist.sort()
        return [point for _, point in dist[:k]]


if __name__ == "__main__":
    s = Solution()

    def normalize(pts):
        return sorted([sorted(p) for p in pts])

    assert normalize(s.kClosest([[1, 3], [-2, 2]], 1)) == \
        normalize([[-2, 2]])                                       # Example 1
    assert normalize(s.kClosest([[3, 3], [5, -1], [-2, 4]], 2)) == \
        normalize([[3, 3], [-2, 4]])                               # Example 2

    print("k_closest_origin.py: all tests passed")
