"""
LeetCode 2390 - Removing Stars From a String (Medium)
https://leetcode.com/problems/removing-stars-from-a-string/

You are given a string s, which contains stars *. In one operation,
you can:
  - Choose a star in s.
  - Remove the closest non-star character to its left, as well as
    remove the star itself.
Return the string after all stars have been removed. The input is
generated such that the operation is always possible.

Solution idea:
  Right-to-left walk. Each '*' increments a pending "skip" counter; for
  any letter, if the counter is positive consume one (i.e., this letter
  pairs with a star to its right) else emit the letter into `res`. The
  result is built reversed, so reverse it before returning.
"""


class Solution:
    def removeStars(self, s: str) -> str:
        res = ""
        star_counter = 0
        for ch in s[::-1]:
            if ch == "*":
                star_counter += 1
            elif star_counter > 0:
                star_counter -= 1
            else:
                res += ch
        return res[::-1]


if __name__ == "__main__":
    s = Solution()

    assert s.removeStars("leet**cod*e") == "lecoe"     # Example 1
    assert s.removeStars("erase*****") == ""           # Example 2

    print("replace_stars.py: all tests passed")
