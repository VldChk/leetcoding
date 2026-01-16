"""
Given a string s and an integer k, reverse the first k characters for every 2k characters counting from the start of the string.

If there are fewer than k characters left, reverse all of them. If there are less than 2k but greater than or equal to k characters, then reverse the first k characters and leave the other as original.
"""


class Solution:
    def reverseStr(self, s: str, k: int) -> str:
        r = str()
        for i in range(len(s) // (2 * k) + 1):
            sl = s[2 * k * i : (2 * k) * (i + 1)]
            r = r + sl[:k][::-1] + sl[k:]
        return r
