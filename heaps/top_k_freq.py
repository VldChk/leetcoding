"""
LeetCode 347 - Top K Frequent Elements (Medium)
https://leetcode.com/problems/top-k-frequent-elements/

Given an integer array nums and an integer k, return the k most frequent
elements. You may return the answer in any order.

Constraints note: solution must run better than O(n log n) for full
credit, though LC accepts any correct answer.

Solution idea:
  Count frequencies in a dict, then use heapq.nlargest to grab the top k
  by (frequency, value) pairs. Strip out the values from the result.
  Total time O(n log k) for the heap step plus O(n) for counting.
"""
from typing import List
import heapq

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        d: dict[int, int] = {}
        for n in nums:
            d[n] = d.get(n, 0) + 1
        top_k = heapq.nlargest(k, [(v, k) for k,v in d.items()])
        return [i[1] for i in top_k]


if __name__ == "__main__":
    s = Solution()

    # LeetCode accepts the result in any order.
    assert sorted(s.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]   # Example 1
    assert sorted(s.topKFrequent([1], 1)) == [1]                     # Example 2

    print("top_k_freq.py: all tests passed")
