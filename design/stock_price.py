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
