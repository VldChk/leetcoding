"""
LeetCode 1756 - Design Most Recently Used Queue (Medium, Premium)
https://leetcode.com/problems/design-most-recently-used-queue/

Design a queue-like structure initialised with the elements
[1, 2, ..., n]. Implement:
  * MRUQueue(int n) — build the queue [1, 2, ..., n].
  * fetch(int k)    — move the k-th element (1-indexed) to the end of
                      the queue and return its value.

Example:
  MRUQueue(8); fetch(3)=3, fetch(5)=6, fetch(2)=2, fetch(8)=2
  -> outputs [null, 3, 6, 2, 2]

Solution idea:
  Back the queue with a plain list: fetch pops index k-1 and appends the
  value, which is O(n) per call — simple and fine for the constraints.
  (A Fenwick tree / sqrt-decomposition layout would reach O(log n) /
  O(sqrt n) per fetch, but is overkill here.)
"""

class MRUQueue:

    def __init__(self, n: int):
        self.mqueue = [i for i in range(1, n+1)]

    def fetch(self, k: int) -> int:
        t = self.mqueue[k-1]
        self.mqueue.pop(k-1)
        self.mqueue.append(t)
        return t 
        


# Your MRUQueue object will be instantiated and called as such:
# obj = MRUQueue(n)
# param_1 = obj.fetch(k)

if __name__ == "__main__":
    # Official example
    q = MRUQueue(8)
    assert q.fetch(3) == 3
    assert q.fetch(5) == 6
    assert q.fetch(2) == 2
    assert q.fetch(8) == 2

    # Fetch the head, then an already-last element, then the head again
    q2 = MRUQueue(3)
    assert q2.fetch(1) == 1          # [2, 3, 1]
    assert q2.fetch(3) == 1          # 1 is already last -> stays, returns 1
    assert q2.fetch(1) == 2          # [3, 1, 2]

    print("most_recent_queue.py: all tests passed")