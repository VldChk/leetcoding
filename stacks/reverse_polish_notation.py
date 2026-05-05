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
        