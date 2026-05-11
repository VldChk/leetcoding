"""
LeetCode 295 - Find Median from Data Stream (Hard)
https://leetcode.com/problems/find-median-from-data-stream/

The median is the middle value in an ordered integer list. If the size
of the list is even, the median is the average of the two middle values.

Implement the MedianFinder class:
  - MedianFinder() initializes the MedianFinder object.
  - void addNum(int num) adds the integer num from the data stream.
  - double findMedian() returns the median of all elements so far.
  Answers within 10^-5 of the actual answer will be accepted.

Solution idea:
  Keep two heaps: a max-heap `__low` holding the smaller half and a
  min-heap `__high` holding the larger half. Maintain the invariant
  len(__low) == len(__high) or len(__low) == len(__high)+1 (low gets
  the extra element when the total is odd). To insert, route the new
  number through the opposite heap to rebalance: when sizes are equal,
  push into low via heappushpop on high; when low is one larger, push
  into high via heappushpop_max on low. Median is low[0] when sizes
  differ, or (low[0] + high[0]) / 2 when they match.

Note: uses heapq.heappush_max / heappushpop_max which are Python 3.14+
public API. LeetCode's runtime supports them; the test block below
includes a polyfill so the file is also runnable on Python 3.13.
"""
import heapq
class MedianFinder:

    def __init__(self):
        self.__low: list[int] = []
        self.__high: list[int] = []
        

    def addNum(self, num: int) -> None:
        if len(self.__low) == len(self.__high):
            heapq.heappush_max(self.__low, heapq.heappushpop(self.__high, num))
        else:
            heapq.heappush(self.__high, heapq.heappushpop_max(self.__low, num))
        

    def findMedian(self) -> float:
        if len(self.__low) == len(self.__high):
            return float(self.__low[0] + self.__high[0])/ 2 
        else:
            return self.__low[0]


# Your MedianFinder object will be instantiated and called as such:
# obj = MedianFinder()
# obj.addNum(num)
# param_2 = obj.findMedian()


if __name__ == "__main__":
    # Polyfill for Python <3.14 — heapq.heappush_max and heappushpop_max
    # are Python 3.14+ public API. The private _siftdown_max / _siftup_max
    # primitives have been in heapq for a long time, so we can rebuild
    # the missing public helpers without touching the solution.
    if not hasattr(heapq, "heappush_max"):
        def _heappush_max(heap, item):
            heap.append(item)
            heapq._siftdown_max(heap, 0, len(heap) - 1)

        def _heappushpop_max(heap, item):
            if heap and heap[0] > item:
                item, heap[0] = heap[0], item
                heapq._siftup_max(heap, 0)
            return item

        heapq.heappush_max = _heappush_max
        heapq.heappushpop_max = _heappushpop_max

    # LeetCode example 1
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0

    print("median_of_stream.py: all tests passed")