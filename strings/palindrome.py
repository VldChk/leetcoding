class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        x_s = str(x)
        n = len(x_s)
        k = len(x_s) // 2
        return all([x_s[i] == x_s[n-i-1] for i in range(0, k+1)])
        