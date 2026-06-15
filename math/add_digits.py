"""
LeetCode 258 - Add Digits (Easy)
https://leetcode.com/problems/add-digits/

Given an integer num, repeatedly sum its digits until the result is a
single digit, and return that digit (the digital root).

Example:
  num = 38 -> 3 + 8 = 11 -> 1 + 1 = 2 -> return 2
  num = 0  -> 0

Solution idea:
  Straightforward iterative digit-summing: while the value still has two
  or more digits, replace it by the sum of its digits. A handful of
  passes, each O(number of digits). (The classic O(1) closed form is the
  digital root 1 + (num - 1) % 9 for num > 0, but the explicit loop is
  kept here.)
"""
class Solution:
    def addDigits(self, num: int) -> int:
        r = num
        while r >= 10:
            r = 0
            while num > 0:
                r += num % 10
                num //= 10
            num = r
        return r


if __name__ == "__main__":
    s = Solution()

    assert s.addDigits(38) == 2      # 38 -> 11 -> 2
    assert s.addDigits(0) == 0
    assert s.addDigits(9) == 9
    assert s.addDigits(199) == 1     # 199 -> 19 -> 10 -> 1

    print("add_digits.py: all tests passed")
