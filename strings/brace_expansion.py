"""
LeetCode 1087 - Brace Expansion (Medium, Premium)
https://leetcode.com/problems/brace-expansion/

You are given a string s representing a list of words. Each letter in
the word has one or more options. If there is one option, the letter is
represented as is. If there is more than one option, then curly braces
delimit the options, e.g., "{a,b,c}" represents options ["a", "b", "c"].

Return all words that can be formed in this manner, sorted in
lexicographical order.

Solution idea:
  Build the expansion incrementally in `res`, starting with [""]. Walk
  the string left to right: for a literal character, append it to every
  word so far. For a "{...}" group, parse the comma-separated options,
  sort them alphabetically (ensuring final lexicographic order without
  a final sort step), and Cartesian-product them onto every existing
  partial word.
"""
from typing import List
class Solution:
    def expand(self, s: str) -> List[str]:
        i = 0
        res: List[str] = [""]
        while i < len(s):
            if s[i] != "{":
                res = [r + s[i] for r in res]
            else:
                i += 1
                options: List[str] = []
                while s[i] != "}":
                    if s[i] == ",":
                        i += 1
                        continue
                    options.append(s[i])
                    i += 1
                options.sort()
                res = [r + o for r in res for o in options]
            i += 1
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.expand("{a,b}c{d,e}f") == ["acdf", "acef", "bcdf", "bcef"]   # Example 1
    assert s.expand("abcd") == ["abcd"]                                   # Example 2

    print("brace_expansion.py: all tests passed")