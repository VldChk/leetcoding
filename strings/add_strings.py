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
