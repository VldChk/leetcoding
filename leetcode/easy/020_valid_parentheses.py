"""
LeetCode 20: Valid Parentheses
https://leetcode.com/problems/valid-parentheses/

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

Time Complexity: O(n)
Space Complexity: O(n)
"""


class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        bracket_map = {")": "(", "}": "{", "]": "["}

        for char in s:
            if char in bracket_map:
                # It's a closing bracket
                if not stack or stack[-1] != bracket_map[char]:
                    return False
                stack.pop()
            else:
                # It's an opening bracket
                stack.append(char)

        return len(stack) == 0


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    assert solution.isValid("()") is True

    # Test case 2
    assert solution.isValid("()[]{}") is True

    # Test case 3
    assert solution.isValid("(]") is False

    # Test case 4
    assert solution.isValid("([)]") is False

    # Test case 5
    assert solution.isValid("{[]}") is True

    # Test case 6: empty string
    assert solution.isValid("") is True

    print("All test cases passed!")
