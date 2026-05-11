"""
LeetCode 150 - Evaluate Reverse Polish Notation (Medium)
https://leetcode.com/problems/evaluate-reverse-polish-notation/

You are given an array of strings `tokens` that represents an arithmetic
expression in Reverse Polish Notation. Evaluate the expression. Return
an integer that represents the value of the expression.

Operators are +, -, *, /. Operands are integers. Each operation between
two operands is valid. Division between two integers always truncates
toward zero.

Solution idea:
  Standard stack evaluator. Push integer tokens; when an operator
  appears, pop the two most recent values (right operand on top, left
  operand below) and push the result. `math.trunc(a/b)` implements
  truncation toward zero (Python's `//` would truncate toward -inf and
  give wrong answers for mixed-sign divisions). Final stack-top is the
  expression value.
"""
import math
from typing import List
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        signs = ["+", "*", "/", "-"]
        stack: list[int] = []
        for token in tokens:
            if token not in signs:
                stack.append(int(token))
            else:
                one = stack.pop()
                two = stack.pop()
                if token == "+":
                    stack.append(two + one)
                elif token == "*":
                    stack.append(two * one)
                elif token == "-":
                    stack.append(two-one)
                else:
                    stack.append(math.trunc(two/one))
        return stack[-1]


if __name__ == "__main__":
    s = Solution()

    assert s.evalRPN(["2", "1", "+", "3", "*"]) == 9                   # Example 1
    assert s.evalRPN(["4", "13", "5", "/", "+"]) == 6                  # Example 2
    assert s.evalRPN(["10", "6", "9", "3", "+", "-11", "*", "/", "*",
                      "17", "+", "5", "+"]) == 22                       # Example 3

    print("reverse_polish_notation.py: all tests passed")
