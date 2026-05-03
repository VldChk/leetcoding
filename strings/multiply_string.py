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
        
        