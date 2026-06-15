"""
LeetCode 356 - Line Reflection (Medium, Premium)
https://leetcode.com/problems/line-reflection/

Given n points on a 2D plane, determine whether there exists a vertical
line (parallel to the y-axis) such that reflecting every point across it
maps the set of points onto itself. Duplicate points are allowed and do
not change the answer.

If such a line x = c exists it must satisfy c = (min_x + max_x) / 2,
because the leftmost and rightmost points have to map onto each other.

Examples:
  points = [[1, 1], [-1, 1]]   -> True   (axis x = 0)
  points = [[1, 1], [-1, -1]]  -> False

Solution idea:
  Sort and de-duplicate the points, take the candidate axis at
  coord = min_x + (max_x - min_x) / 2, and require equally many points on
  each side. Walk the left half outward-in against the reversed right
  half, checking each pair shares its y and mirrors its x about the axis;
  points sitting exactly on the axis are skipped. O(n log n) for the
  sort. (An equivalent O(n) check just asks whether (2c - x, y) is in a
  hash set for every point — that is what the reference checker uses.)
"""
from typing import List
class Solution:
    def isReflected(self, points: List[List[int]]) -> bool:
        
        points.sort(key=lambda x: (x[0], x[1]))
        new_points = [points[0]]
        i = 1 
        while i < len(points):
            if tuple(points[i-1]) == tuple(points[i]):
                i += 1
                continue
            else:
                new_points.append(points[i])
                i += 1
        points = new_points
        coord = points[0][0] + (points[-1][0] - points[0][0]) / 2
        
        if sum(1 for x in points if x[0] < coord) != sum(1 for x in points if x[0] > coord):
            return False
        
        points = [x for x in points if x[0] != coord]
        
        i = 0
        k = len(points) // 2
        
        first_half = points[:k]
        if len(points) % 2 == 1:
            second_half = points[(k+1):]
        else:
            second_half = points[k:]
        second_half.sort(key=lambda x: (x[0], -x[1]))
        j = len(second_half) - 1

        while i < len(first_half) and j >= 0:
            if first_half[i][0] == second_half[j][0]:
                i += 1
                j -= 1
                continue
            if (coord - first_half[i][0]) != (second_half[j][0] - coord):
                return False
            if first_half[i][1] != second_half[j][1]:
                return False
            i += 1
            j -= 1
        if len(points) % 2 == 1:
            if points[k][0] != coord:
                return False
        return True


if __name__ == "__main__":
    s = Solution()

    # Official examples
    assert s.isReflected([[1, 1], [-1, 1]]) is True
    assert s.isReflected([[1, 1], [-1, -1]]) is False
    # Single point is always reflectable; point on the axis is fine
    assert s.isReflected([[0, 0]]) is True
    assert s.isReflected([[1, 1], [-1, 1], [0, 0]]) is True
    # Mismatched y across the axis
    assert s.isReflected([[1, 1], [2, 2]]) is False
    # Duplicates do not break it
    assert s.isReflected([[1, 1], [-1, 1], [1, 1]]) is True

    print("line_reflection.py: all tests passed")