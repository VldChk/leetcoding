from typing import List
import heapq

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        d: dict[int, int] = {}
        for n in nums:
            d[n] = d.get(n, 0) + 1
        top_k = heapq.nlargest(k, [(v, k) for k,v in d.items()])
        return [i[1] for i in top_k]
        
        