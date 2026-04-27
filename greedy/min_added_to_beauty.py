class Solution:
    def makeIntegerBeautiful(self, n: int, target: int) -> int:
        split = []
        i = n
        while i > 0:
            split.append(i % 10)
            i = i // 10
        if sum(split) <= target:
            return 0
        res = []
        for idx, j in enumerate(split):
            if idx == 0:
                res.append(10 - j)
            else:
                res.append(10 - j - 1)
            if sum(split[idx + 1 :]) + 1 <= target:
                break
        if sum(split[idx + 1 :]) > target:
            res[-1] -= 1

        r = 0
        for i, k in enumerate(res):
            r += k * (10**i)
        return r
