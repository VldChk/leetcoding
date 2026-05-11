"""
LeetCode 42 - Trapping Rain Water (Hard)
https://leetcode.com/problems/trapping-rain-water/

Given n non-negative integers representing an elevation map where the
width of each bar is 1, compute how much water it can trap after
raining.

Solution idea (this implementation, monotonic stack with twists):
  Skip leading zeros. Maintain a stack representing a decreasing-then-
  bouncing wall pattern. For each new bar:
    - If it's not taller than the stack top, push it (extend the wall
      on the right side).
    - If it's taller, water gets trapped. Two sub-cases:
      (a) The new bar is taller than the *first* (leftmost) bar of the
          stack — collapse: pop while the popped values are below the
          stack[0] level, adding (stack[0] - popped) per cell, then
          reset the stack to [new_bar].
      (b) Otherwise the new bar only fills part of the basin — walk
          back from the top, raising each lower entry to the new bar's
          height while crediting (new_bar - old) per raised cell, and
          push the new bar.
  The result is the total trapped volume. Equivalent to the textbook
  two-pointer approach, just expressed as a stack-walk.
"""
from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        start_idx = 0
        res = 0
        while start_idx < len(height) and height[start_idx] == 0:
            start_idx += 1
        
        stack: List[int] = []

        for i in range(start_idx, len(height)):
            if not stack:
                stack.append(height[i])
                continue
            
            if height[i] <= stack[-1]:
                stack.append(height[i])
            elif height[i] > stack[-1]:
                if stack[0] < height[i]:
                    while len(stack) > 1 and height[i] > stack[-1] and stack[-1] < stack[0]:
                        res += (stack[0] - stack[-1])
                        stack.pop()
                    stack = []
                    stack.append(height[i])
                else:
                    j = len(stack) - 1
                    while j > 0 and height[i] > stack[j]:
                        res += (height[i] - stack[j])
                        stack[j] = height[i]
                        j -= 1
                    stack.append(height[i])
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6   # Example 1
    assert s.trap([4, 2, 0, 3, 2, 5]) == 9                     # Example 2

    print("trap_water.py: all tests passed")
