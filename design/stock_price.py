"""
LeetCode 2034 - Stock Price Fluctuation (Medium)
https://leetcode.com/problems/stock-price-fluctuation/

You are given a stream of records about a particular stock. Each record
contains a timestamp and the corresponding price of the stock at that
timestamp.

Records are not necessarily in chronological order, and may correct an
earlier record (same timestamp, new price overrides the old one).

Implement the StockPrice class:
  - StockPrice()                         initializes the object.
  - void update(int timestamp, int price) updates the price at timestamp.
  - int current()                        returns the latest price at the
                                          most recent timestamp.
  - int maximum()                        returns the maximum price
                                          across all corrected records.
  - int minimum()                        returns the minimum price.

Solution idea:
  Keep `self._ticks` as a dict timestamp -> latest price, plus a min-heap
  and a max-heap of (price, timestamp) entries. Stale heap entries (where
  _ticks[ts] no longer matches the heap's stored price) are lazily evicted
  from the top of the relevant heap when querying min/max. `current` is
  trivial: track the most-recent timestamp in `_latest_ts` on update and
  look up its current price in the dict.

Note: uses heapq.heappush_max / heappop_max which are Python 3.14+ public
API. The test block polyfills them for earlier Pythons.
"""
import bisect
import heapq
class StockPrice:

    def __init__(self):
        self._ticks = {}
        self._min_prices = []
        self._max_prices = []
        self._latest_ts = -1
        

    def update(self, timestamp: int, price: int) -> None:
        if self._ticks.get(timestamp, -1) == price:
            return
        self._latest_ts = max(self._latest_ts, timestamp)
        self._ticks[timestamp] = price

        heapq.heappush(self._min_prices, (price, timestamp))
        heapq.heappush_max(self._max_prices, (price, timestamp))
        return


    def current(self) -> int:
        ts = self._latest_ts
        return self._ticks[ts]

    def maximum(self) -> int:
        while True:
            max_price, ts = self._max_prices[0]
            if self._ticks[ts] != max_price:
                heapq.heappop_max(self._max_prices)
                continue
            else:
                return max_price
        return -1
        

    def minimum(self) -> int:
        while True:
            min_price, ts = self._min_prices[0]
            if self._ticks[ts] != min_price:
                heapq.heappop(self._min_prices)
                continue
            else:
                return min_price
        return 2**31-1
        


# Your StockPrice object will be instantiated and called as such:
# obj = StockPrice()
# obj.update(timestamp,price)
# param_2 = obj.current()
# param_3 = obj.maximum()
# param_4 = obj.minimum()


if __name__ == "__main__":
    # Polyfill Python <3.14 public max-heap helpers (LeetCode's runtime
    # has them; the local interpreter may not).
    if not hasattr(heapq, "heappush_max"):
        def _heappush_max(heap, item):
            heap.append(item)
            heapq._siftdown_max(heap, 0, len(heap) - 1)

        heapq.heappush_max = _heappush_max
    if not hasattr(heapq, "heappop_max"):
        heapq.heappop_max = heapq._heappop_max  # private function exists already

    # LeetCode example 1
    sp = StockPrice()
    sp.update(1, 10)              # timestamps={1:10}
    sp.update(2, 5)               # timestamps={1:10, 2:5}
    assert sp.current() == 5      # latest ts=2 -> 5
    assert sp.maximum() == 10     # max across all -> 10
    sp.update(1, 3)               # correct ts=1 to 3
    assert sp.maximum() == 5      # max now 5
    sp.update(4, 2)               # timestamps={1:3, 2:5, 4:2}
    assert sp.minimum() == 2

    print("stock_price.py: all tests passed")
