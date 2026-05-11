"""
LeetCode 394 - Decode String (Medium)
https://leetcode.com/problems/decode-string/

Given an encoded string, return its decoded string. The encoding rule is:
k[encoded_string], where the encoded_string inside the square brackets
is being repeated exactly k times. Note that k is guaranteed to be a
positive integer.

You may assume that the input string is always valid; there are no extra
white spaces, square brackets are well-formed, etc. Furthermore, you
may assume that the original data does not contain any digits and that
digits are only for those repeat numbers, k.

Solution idea:
  Recursive descent parser. The outer loop walks the string and on
  digits delegates to `_recursive_parsing(s, i)` which (1) reads the
  multi-digit count `num`, (2) skips the '[' bracket, (3) accumulates
  body characters and recurses on any nested digit it meets, and
  (4) on ']' returns res * num and the index past the bracket.
"""


class Solution:
    def decodeString(self, s: str) -> str:
        def _recursive_parsing(s: str, i: int) -> tuple[str, int]:
            res: str = ""
            num = 0
            while s[i].isnumeric():
                num = (num*10) + int(s[i])
                i += 1
            i += 1
            while s[i] != "]":
                if s[i].isnumeric():
                    t, i = _recursive_parsing(s, i)
                    res += t
                else:
                    res += s[i]
                    i += 1
           
            i += 1
            
            return res * num, i
        
        j = 0
        res: str = ""
        while j < len(s):
            if s[j].isnumeric():
                t, j = _recursive_parsing(s, j)
                res += t
            else:
                res += s[j]
                j += 1
        
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.decodeString("3[a]2[bc]") == "aaabcbc"                # Example 1
    assert s.decodeString("3[a2[c]]") == "accaccacc"               # Example 2
    assert s.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"     # Example 3

    print("decode_strings.py: all tests passed")
