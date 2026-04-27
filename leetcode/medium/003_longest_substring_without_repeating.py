"""
LeetCode 3: Longest Substring Without Repeating Characters
https://leetcode.com/problems/longest-substring-without-repeating-characters/

Given a string s, find the length of the longest substring without repeating
characters.

Time Complexity: O(n)
Space Complexity: O(min(m, n)) where m is the size of the character set
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        char_index = {}
        max_length = 0
        start = 0

        for end, char in enumerate(s):
            if char in char_index and char_index[char] >= start:
                start = char_index[char] + 1
            char_index[char] = end
            max_length = max(max_length, end - start + 1)

        return max_length


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    assert solution.lengthOfLongestSubstring("abcabcbb") == 3

    # Test case 2
    assert solution.lengthOfLongestSubstring("bbbbb") == 1

    # Test case 3
    assert solution.lengthOfLongestSubstring("pwwkew") == 3

    # Test case 4: empty string
    assert solution.lengthOfLongestSubstring("") == 0

    # Test case 5: single character
    assert solution.lengthOfLongestSubstring("a") == 1

    # Test case 6: all unique
    assert solution.lengthOfLongestSubstring("abcdef") == 6

    print("All test cases passed!")
