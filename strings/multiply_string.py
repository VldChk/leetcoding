"""
LeetCode 43 - Multiply Strings (Medium)
https://leetcode.com/problems/multiply-strings/

Given two non-negative integers num1 and num2 represented as strings,
return the product of num1 and num2, also represented as a string.

Note: You must not use any built-in BigInteger library or convert the
inputs to integer directly.

Solution idea:
  Schoolbook multiplication digit by digit. Reverse both strings so
  position 0 holds the least significant digit. The outer loop iterates
  digits of `num1`, the inner loop iterates digits of `num2`; the digit
  product plus the running carry lands at index i+j of the result. If
  the slot already has a partial sum from a previous iteration, fold
  the new contribution in and update carry. Reverse the result and join.
"""


class Solution:

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        if len(num1) > len(num2):
            num1, num2 = num2, num1 # we prefer outer loop for smaller int
        num1, num2 = num1[::-1], num2[::-1]
        res: list[int] = []
        for i in range(len(num1)):
            in_memory = 0
            for j in range(len(num2)):
                t = int(num1[i]) * int(num2[j]) + in_memory
                if i+j >= len(res):
                    res.append(t % 10)
                    in_memory = t // 10
                else:
                    in_memory = (t + res[i+j]) // 10
                    res[i+j] = (t + res[i+j]) % 10
            if in_memory > 0:
                res.append(in_memory)
                    
        res = res[::-1]
        return ''.join([str(n) for n in res])


if __name__ == "__main__":
    s = Solution()

    assert s.multiply("2", "3") == "6"               # Example 1
    assert s.multiply("123", "456") == "56088"       # Example 2
    assert s.multiply("0", "1234") == "0"            # zero short-circuit

    print("multiply_string.py: all tests passed")
        