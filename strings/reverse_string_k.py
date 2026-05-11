"""
LeetCode 541 - Reverse String II (Easy)
https://leetcode.com/problems/reverse-string-ii/

Given a string s and an integer k, reverse the first k characters for
every 2k characters counting from the start of the string.

If there are fewer than k characters left, reverse all of them. If
there are less than 2k but greater than or equal to k characters, then
reverse the first k characters and leave the other as original.

Solution idea:
  Slice the string into chunks of length 2k, then for each chunk emit
  reversed(chunk[:k]) + chunk[k:]. The slicing handles the trailing
  short chunk automatically: if fewer than k chars remain, chunk[:k] is
  the whole tail (still reversed) and chunk[k:] is empty.
"""


class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        r = str()
        for i in range(len(s) // (2 * k) + 1):
            sl = s[2 * k * i : (2 * k) * (i + 1)]
            r = r + sl[:k][::-1] + sl[k:]
        return r


if __name__ == "__main__":
    s = Solution()

    assert s.reverseStr("abcdefg", 2) == "bacdfeg"     # Example 1
    assert s.reverseStr("abcd", 2) == "bacd"           # Example 2

    print("reverse_string_k.py: all tests passed")
