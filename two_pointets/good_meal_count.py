from typing import List
class Solution:
    def countPairs(self, deliciousness: List[int]) -> int:
        deliciousness.sort()
        twos = [2**i for i in range(0, 22) if 2**i >= min(deliciousness) * 2 and 2**i <= max(deliciousness) * 2]
        d: dict[int, int] = {}
        for n in deliciousness:
            d[n] = d.get(n, 0) + 1
        res = 0
        for k, v in d.items():
            for t in twos:
                if (t-k) < k:
                    continue
                if k == t-k:
                    res += v * (v - 1) // 2
                elif t - k in d:
                    res += (v * d[t - k])

        return res % (10**9 + 7)