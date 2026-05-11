"""
LeetCode 844 - Backspace String Compare (Easy)
https://leetcode.com/problems/backspace-string-compare/

Given two strings s and t, return true if they are equal when both are
typed into empty text editors. '#' means a backspace character.

Note that after backspacing an empty text, the text will continue empty.

Follow up: Can you solve it in O(n) time and O(1) space?

Solution idea:
  Walk both strings right to left in lockstep, lazily resolving '#'
  backspaces. Each time you see '#', bump that side's `skip` counter;
  for any letter, if skip > 0 consume one (the letter is erased) and
  keep walking, otherwise that letter is the next "real" character to
  compare. After both inner skip-loops settle, compare the candidate
  characters; mismatch -> return False. Continue until both pointers
  cross zero. O(n) time, O(1) extra space.
"""


class Solution(object):
    def backspaceCompare(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        i = len(s) - 1
        j = len(t) - 1
        skip_s = 0
        skip_t = 0

        while i >= 0 or j >= 0:
            while i >= 0:
                if s[i] == '#':
                    skip_s += 1
                    i -= 1
                elif skip_s > 0:
                    skip_s -= 1
                    i -= 1
                else:
                    break 
            while j >= 0:
                if t[j] == '#':
                    skip_t += 1
                    j -= 1
                elif skip_t > 0:
                    skip_t -= 1
                    j -= 1
                else:
                    break

            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:
                return False

            i -= 1
            j -= 1

        return True


if __name__ == "__main__":
    s = Solution()

    assert s.backspaceCompare("ab#c", "ad#c") is True       # Example 1
    assert s.backspaceCompare("ab##", "c#d#") is True       # Example 2
    assert s.backspaceCompare("a#c", "b") is False          # Example 3

    print("backspaced_strings.py: all tests passed")