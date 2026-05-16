"""
LeetCode 1106 - Parsing A Boolean Expression (Hard)
https://leetcode.com/problems/parsing-a-boolean-expression/

A boolean expression is an expression that evaluates to either true or
false. It can be in one of the following shapes:

  * 't' — that evaluates to true.
  * 'f' — that evaluates to false.
  * '!(subExpr)' — that evaluates to the logical NOT of the inner
    expression subExpr.
  * '&(subExpr1, subExpr2, ..., subExprn)' — that evaluates to the
    logical AND of the inner expressions.
  * '|(subExpr1, subExpr2, ..., subExprn)' — that evaluates to the
    logical OR of the inner expressions.

Given a string expression that represents a boolean expression,
return the evaluation of that expression.

It is guaranteed that the given expression is valid and follows the
given rules.

Solution idea:
  Two-stack parser. `operations` holds pending operators ('&', '|',
  '!'); `booleans` holds a stack of *lists* of accumulated child
  values, one frame per open paren. On '(' push a new empty frame;
  on a literal 't'/'f' append the value to the top frame; on ')'
  pop the operator and frame, reduce with `resolve_expr`, then
  splice the result into the now-top frame. The final answer is
  `booleans[-1][0]`. O(|expression|).
"""
from functools import cache
class Solution:
    @cache
    def parseBoolExpr(self, expression: str) -> bool:
        def resolve_expr(token: str, booleans: list[bool]) -> list[bool]:
            if token == "!":
                return [not b for b in booleans]
            elif token == "|":
                return [any(booleans)]
            else:
                return [all(booleans)]
        tokens = ["!", "|", "&"]
        operations: list[str] = []
        booleans: list[list[bool]] = []
        d = {"t": True, "f": False}
        if len(expression) == 1:
            return d[expression[0]]
        i = 0
        while i < len(expression):
            e = expression[i]
            if e in tokens:
                operations.append(e)
                i += 1
            elif e == "(":
                i += 1
                booleans.append([])
                while expression[i] != ")" and expression[i] not in tokens:
                    if expression[i] == ",":
                        i += 1
                        continue
                    booleans[-1].append(d[expression[i]])
                    i += 1
            elif e == ")":
                if operations:
                    o = operations.pop()
                    b = booleans.pop()
                    b = resolve_expr(o, b)
                    if booleans:
                        booleans[-1].extend(b)
                    else:
                        booleans = [b]
                else:
                    continue
                i += 1
            elif e in d:
                booleans[-1].append(d[e])
                i += 1
            else:
                i += 1
        return booleans[-1][0]


if __name__ == "__main__":
    s = Solution()

    assert s.parseBoolExpr("&(|(f))") == False              # Example 1
    assert s.parseBoolExpr("|(f,f,f,t)") == True             # Example 2
    assert s.parseBoolExpr("!(&(f,t))") == True              # Example 3

    print("parsing_boolean_expr.py: all tests passed")
