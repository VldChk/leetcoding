"""
LeetCode 9: Palindrome Number
https://leetcode.com/problems/palindrome-number/

Given an integer x, return true if x is a palindrome, and false otherwise.

Time Complexity: O(log n) - we process half of the digits
Space Complexity: O(1)
"""


class Solution:
    def isPalindrome(self, x: int) -> bool:
        # Negative numbers are not palindromes
        # Numbers ending with 0 (except 0 itself) are not palindromes
        if x < 0 or (x % 10 == 0 and x != 0):
            return False

        reversed_half = 0
        while x > reversed_half:
            reversed_half = reversed_half * 10 + x % 10
            x //= 10

        # For odd-length numbers, we need to remove the middle digit
        return x == reversed_half or x == reversed_half // 10


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1: 121 is a palindrome
    assert solution.isPalindrome(121) is True

    # Test case 2: -121 is not a palindrome
    assert solution.isPalindrome(-121) is False

    # Test case 3: 10 is not a palindrome
    assert solution.isPalindrome(10) is False

    # Test case 4: 0 is a palindrome
    assert solution.isPalindrome(0) is True

    # Test case 5: single digit
    assert solution.isPalindrome(7) is True

    print("All test cases passed!")
