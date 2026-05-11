"""
LeetCode 781 - Rabbits in Forest (Medium)
https://leetcode.com/problems/rabbits-in-forest/

There is a forest with an unknown number of rabbits. We asked n rabbits
"how many rabbits have the same color as you?" and collected the answers
in an integer array `answers` where `answers[i]` is the answer of the
i-th rabbit.

Given the array `answers`, return the minimum number of rabbits that
could be in the forest.

Solution idea:
  Group rabbits by their answer x. Each group of (x+1) rabbits with the
  same answer can plausibly all be one color, so we only need a new
  group every (x+1) rabbits. `d[x]` tracks the remaining capacity of
  the current open group for answer x; when capacity hits zero we
  commit (x+1) rabbits to the count and start a fresh group. After the
  scan, every still-open group contributes (x+1) more rabbits.
"""
from typing import List
class Solution:
    def numRabbits(self, answers: List[int]) -> int:
        d = {}
        res = 0
        for answer in answers:
            if answer in d:
                d[answer] -= 1
                if d[answer] == 0:
                    res += answer + 1
                    d[answer] = answer + 1
            else:
                d[answer] = answer + 1
        for k in d.keys():
            res += k + 1

        return res


if __name__ == "__main__":
    s = Solution()

    assert s.numRabbits([1, 1, 2]) == 5         # Example 1
    assert s.numRabbits([10, 10, 10]) == 11     # Example 2

    print("count_rabbits.py: all tests passed")