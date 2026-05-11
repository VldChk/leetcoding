"""
LeetCode 239 - Sliding Window Maximum (Hard)
https://leetcode.com/problems/sliding-window-maximum/

You are given an array of integers nums, there is a sliding window of
size k which is moving from the very left of the array to the very
right. You can only see the k numbers in the window. Each time the
sliding window moves right by one position.

Return the max sliding window.

Solution idea (heap + counter, lazy eviction):
  Keep a max-heap of all values currently in or recently in the
  window, plus a Counter tracking how many of each value are *still*
  in the live window. When asked for the current max, lazily evict
  stale heap tops whose live count has dropped to zero. Each slide:
  decrement count of the outgoing element, increment count of the
  incoming, push the incoming onto the heap. Each element is pushed/
  popped at most once -> amortized O(n log n).

Note: uses heapq.heapify_max / heappush_max / heappop_max which are
Python 3.14+ public API. The test block polyfills them on older
Pythons (LeetCode's runtime has them natively).
"""
import heapq
from collections import Counter
from typing import List
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        sliding = nums[:k]
        heapq.heapify_max(sliding)
        res: List[int] = []
        d = Counter(sliding)
        for i in range(k, len(nums)):
            n = nums[i]
            while d[sliding[0]] <= 0:
                mx = heapq.heappop_max(sliding)
            res.append(sliding[0])
            d[nums[i-k]] -= 1
            d[n] += 1
            heapq.heappush_max(sliding, n)
        mx = sliding[0]
        while d[mx] <= 0:
            mx = heapq.heappop_max(sliding)
        res.append(mx)
        return res


if __name__ == "__main__":
    # Polyfill Python <3.14 public max-heap helpers.
    if not hasattr(heapq, "heapify_max"):
        heapq.heapify_max = heapq._heapify_max
    if not hasattr(heapq, "heappop_max"):
        heapq.heappop_max = heapq._heappop_max
    if not hasattr(heapq, "heappush_max"):
        def _heappush_max(heap, item):
            heap.append(item)
            heapq._siftdown_max(heap, 0, len(heap) - 1)
        heapq.heappush_max = _heappush_max

    s = Solution()

    assert s.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == \
        [3, 3, 5, 5, 6, 7]                                # Example 1
    assert s.maxSlidingWindow([1], 1) == [1]              # Example 2

    print("max_sliding_window.py: all tests passed")
