"""
LeetCode 11 - Container With Most Water (Medium)
https://leetcode.com/problems/container-with-most-water/

You are given an integer array height of length n. There are n vertical
lines drawn such that the two endpoints of the i-th line are (i, 0) and
(i, height[i]).

Find two lines that together with the x-axis form a container, such
that the container contains the most water.

Return the maximum amount of water a container can store.

Notice that you may not slant the container.

Solution idea:
  Two pointers from both ends. The water held by the pair is
  width * min(height[left], height[right]). Always advance the shorter
  side inward — moving the taller side could only shrink width without
  raising the limiting wall, so it can never improve the area; moving
  the shorter side might find a taller wall that does. Track the max
  along the way. O(n).
"""
from typing import List
class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxarea = 0
        left = 0
        right = len(height) - 1

        while left < right:
            width = right - left
            maxarea = max(maxarea, min(height[left], height[right]) * width)
            if height[left] <= height[right]:
                left += 1
            else:
                right -= 1

        return maxarea


if __name__ == "__main__":
    s = Solution()

    assert s.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49     # Example 1
    assert s.maxArea([1, 1]) == 1                           # Example 2

    print("max_area.py: all tests passed")