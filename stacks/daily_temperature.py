"""
LeetCode 739 - Daily Temperatures (Medium)
https://leetcode.com/problems/daily-temperatures/

Given an array of integers `temperatures` representing daily temperatures,
return an array `answer` such that `answer[i]` is the number of days you
have to wait after the i-th day to get a warmer temperature. If there is
no future day for which this is possible, set answer[i] = 0.

Solution idea:
  Monotonic-decreasing stack of indices. Walk left to right; when the
  current temperature is hotter than what the stack's top index records,
  pop those indices and write their answer = (current i - popped j).
  Then push the current index. Each index is pushed and popped at most
  once -> O(n).
"""
from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        if len(temperatures) == 1:
            return [0]
        stack: List[int] = []
        n = len(temperatures)
        res: List[int] = [0] * n
        for i, t in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                res[j] = i - j
            stack.append(i)
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == \
        [1, 1, 4, 2, 1, 1, 0, 0]                            # Example 1
    assert s.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]   # Example 2
    assert s.dailyTemperatures([30, 60, 90]) == [1, 1, 0]          # Example 3

    print("daily_temperature.py: all tests passed")