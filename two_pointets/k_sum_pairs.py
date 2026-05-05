from typing import List
class Solution:
    def maxOperations(self, nums: List[int], k: int) -> int:
        d: dict[int, int] = {}
        res = 0
        for n in nums:
            t = k - n
            if t in d:
                res += 1
                if d[t] == 1:
                    del d[t]
                else:
                    d[t] -= 1
            else:
                d[n] = d.get(n, 0) + 1
        return res