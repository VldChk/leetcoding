"""
LeetCode 1249 - Minimum Remove to Make Valid Parentheses (Medium)
https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/

Given a string s of '(' , ')' and lowercase English characters.

Your task is to remove the minimum number of parentheses ('(' or ')',
in any positions) so that the resulting parentheses string is valid
and return any valid string.

Formally, a parentheses string is valid if and only if:
  - It is the empty string, contains only lowercase characters, or
  - It can be written as AB (A concatenated with B), where A and B
    are valid strings, or
  - It can be written as (A), where A is a valid string.

Solution idea:
  Single forward pass with a stack of unmatched (bracket, index) pairs.
  Each '(' pushes; each ')' pops a matching '(' if one is on top, else
  pushes itself as unmatched. After the pass the stack holds exactly
  the indices to delete. A second backward pass copies the original
  characters into res, skipping indices recorded in the stack (peeled
  off the top as we pass them since we walk in matching order). The
  reverse-built result is reversed before return.
"""


class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:
        bracket: list[tuple[str, int]] = []
        for i, ch in enumerate(s):
            if ch == "(":
                bracket.append(("(", i))
            elif ch == ")":
                if bracket and bracket[-1][0] == "(":
                    bracket.pop()
                else:
                    bracket.append((")", i))
        if len(bracket) == 0:
            return s
        
        res: str = ""
        for i in range(len(s)-1, -1, -1):
            ch = s[i]
            if bracket and i == bracket[-1][1]:
                bracket.pop()
            else:
                res += ch
        return res[::-1]


if __name__ == "__main__":
    s = Solution()

    def is_valid(t: str) -> bool:
        depth = 0
        for ch in t:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth < 0:
                    return False
        return depth == 0

    # LC says "return any valid string" with the *minimum* number of
    # removals, so multiple outputs may be correct. Verify by:
    #   (a) the result is a valid parens string, and
    #   (b) its length equals the canonical answer length.

    # Example 1: "lee(t(c)o)de)" -> any of "lee(t(c)o)de", etc.; len 12
    out1 = s.minRemoveToMakeValid("lee(t(c)o)de)")
    assert is_valid(out1) and len(out1) == 12

    # Example 2: "a)b(c)d" -> "ab(c)d"; len 6
    out2 = s.minRemoveToMakeValid("a)b(c)d")
    assert is_valid(out2) and len(out2) == 6

    # Example 3: "))((" -> ""
    assert s.minRemoveToMakeValid("))((") == ""

    print("remove_brackets.py: all tests passed")