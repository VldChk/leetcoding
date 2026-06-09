from math import inf
from typing import List
class Solution:
    def largestEvenSum(self, nums: List[int], k: int) -> int:
        
        odds = []
        evens = []

        for n in nums:
            if n % 2 == 0:
                evens.append(n)
            else:
                odds.append(n)
        
        odds.sort(reverse=True)
        evens.sort(reverse=True)
        
        odds_idx = 0
        evens_idx = 0
        j = 1

        res = 0

        while j <= k:
            if k-j == 0:
                if evens_idx < len(evens):
                    res += evens[evens_idx]
                    return res
                else:
                    return -1
            else:
                if odds_idx + 1 < len(odds):
                    if (k % 2 == 1 and j % 2 == 1) and evens_idx < len(evens):
                        od = sum(odds[odds_idx:(odds_idx + 2)]) + evens[evens_idx]
                    else:
                        od = sum(odds[odds_idx:(odds_idx + 2)])
                else:
                    od = -inf
                
                if evens_idx + 1 < len(evens):
                    if (len(evens) - (evens_idx + 2)) == 0 and k-j > 2:
                        ev = -inf
                    else:
                        ev = sum(evens[evens_idx:(evens_idx + 2)])
                else:
                    ev = -inf
                
                if od == -inf and ev == -inf:
                    return -1
                else:
                    if od >= ev:
                        res += od
                        odds_idx += 2
                        if (k % 2 == 1 and j % 2 == 1)  and evens_idx < len(evens):
                            evens_idx += 1
                            j += 3
                        else:
                            j += 2
                    else:
                        res += ev
                        evens_idx += 2
                        j += 2
        
        return res 
