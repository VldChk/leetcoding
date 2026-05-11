"""
LeetCode 202 - Happy Number (Easy)
https://leetcode.com/problems/happy-number/

Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:
  - Starting with any positive integer, replace the number by the sum
    of the squares of its digits.
  - Repeat the process until the number equals 1 (where it will stay)
    or it loops endlessly in a cycle which does not include 1.
Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.

Solution idea:
  Recursively compute sum-of-squares-of-digits and remember every value
  seen in `mem`. If we ever produce 1 -> happy. If we revisit a value
  already in `mem` -> we're in a cycle and n is not happy.
"""


class Solution:
    def isHappy(self, n: int) -> bool:
        def _recur(n: int) -> bool:
            r = 0
            i = n
            while i > 0:
                r += (i % 10) ** 2
                i = i // 10
            if r == 1:
                return True
            elif r in mem:
                return False
            else:
                mem.add(r)
                return _recur(r)

        mem: set[int] = set()
        return _recur(n)


if __name__ == "__main__":
    s = Solution()

    assert s.isHappy(19) is True       # Example 1: 19 -> 82 -> 68 -> 100 -> 1
    assert s.isHappy(2) is False       # Example 2: cycles forever

    print("happy_number.py: all tests passed")
