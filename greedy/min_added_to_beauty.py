"""
LeetCode 2457 - Minimum Addition to Make Integer Beautiful (Medium)
https://leetcode.com/problems/minimum-addition-to-make-integer-beautiful/

You are given two positive integers n and target. An integer is beautiful
if the sum of its digits is less than or equal to target.

Return the minimum non-negative integer x such that n + x is beautiful.
The input will be generated such that it is always possible to make n
beautiful.

Solution idea:
  Decompose n into digits least-significant-first into `split`. If the
  digit sum already fits, answer is 0. Otherwise carry-round digit by
  digit: zero-out the units digit (cost 10 - d0), then for each higher
  digit add (10 - d - 1) which together with the carry zeros that
  position too. Stop as soon as the remaining (untouched) high digits
  plus the leftover carry-1 already meet target. A final adjustment
  decrements the last carry by 1 if the higher prefix happened to be
  small enough to absorb it. Finally rebuild the integer x from the
  per-digit additions.
"""


class Solution:
    def makeIntegerBeautiful(self, n: int, target: int) -> int:
        split = []
        i = n
        while i > 0:
            split.append(i % 10)
            i = i // 10
        if sum(split) <= target:
            return 0
        res = []
        for idx, j in enumerate(split):
            if idx == 0:
                res.append(10 - j)
            else:
                res.append(10 - j - 1)
            if sum(split[idx + 1 :]) + 1 <= target:
                break
        if sum(split[idx + 1 :]) > target:
            res[-1] -= 1

        r = 0
        for i, k in enumerate(res):
            r += k * (10**i)
        return r


if __name__ == "__main__":
    s = Solution()

    assert s.makeIntegerBeautiful(16, 6) == 4         # Example 1: 16+4=20
    assert s.makeIntegerBeautiful(467, 6) == 33       # Example 2: 467+33=500
    assert s.makeIntegerBeautiful(1, 1) == 0          # Example 3

    print("min_added_to_beauty.py: all tests passed")
