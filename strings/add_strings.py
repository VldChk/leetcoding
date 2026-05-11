"""
LeetCode 415 - Add Strings (Easy)
https://leetcode.com/problems/add-strings/

Given two non-negative integers, num1 and num2 represented as string,
return the sum of num1 and num2 as a string.

You must solve the problem without using any built-in library for
handling large integers (such as BigInteger). You must also not convert
the inputs to integers directly.

Solution idea:
  Pad the shorter number with leading zeros so the two strings line up.
  Walk both right to left summing digit pairs plus a running carry,
  pushing each digit modulo 10 onto `res` and updating carry as integer
  division by 10. After the loop, push 1 if carry is still set, then
  reverse and join.
"""


class Solution:
    def addStrings(self, num1: str, num2: str) -> str:
        res: list[int] = []
        if len(num1) > len(num2):
            num1, num2 = num2, num1 #swap to min
        m = len(num2) - len(num1)
        num1 = "0"*m + num1
        in_memory = 0
        for i in range(len(num1)-1,-1,-1):
            t: int = int(num1[i]) + int(num2[i]) + in_memory
            res.append(t % 10)
            in_memory = t // 10
        
        if in_memory > 0:
            res.append(1)
        
        return ''.join(str(res[i]) for i in range(len(res)-1,-1,-1))


if __name__ == "__main__":
    s = Solution()

    assert s.addStrings("11", "123") == "134"      # Example 1
    assert s.addStrings("456", "77") == "533"      # Example 2
    assert s.addStrings("0", "0") == "0"           # Example 3

    print("add_strings.py: all tests passed")
