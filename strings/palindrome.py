"""
LeetCode 9 - Palindrome Number (Easy)
https://leetcode.com/problems/palindrome-number/

Given an integer x, return true if x is a palindrome, and false
otherwise.

Solution idea:
  Negative numbers can never be palindromes (the leading minus has no
  trailing match). Convert x to a string and check the first half
  against the mirrored back half. The "middle" character of an odd-
  length number compares with itself, which is harmless.
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        x_s = str(x)
        n = len(x_s)
        k = len(x_s) // 2
        return all([x_s[i] == x_s[n-i-1] for i in range(0, k+1)])


if __name__ == "__main__":
    s = Solution()

    assert s.isPalindrome(121) is True       # Example 1
    assert s.isPalindrome(-121) is False     # Example 2
    assert s.isPalindrome(10) is False       # Example 3

    print("palindrome.py: all tests passed")
