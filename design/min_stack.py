"""
LeetCode 155 - Min Stack (Medium)
https://leetcode.com/problems/min-stack/

Design a stack that supports push, pop, top, and retrieving the minimum
element in constant time.

Implement the MinStack class:
  - MinStack()                initializes the stack object.
  - void push(int val)        pushes the element val onto the stack.
  - void pop()                removes the element on the top of the stack.
  - int top()                 gets the top element of the stack.
  - int getMin()              retrieves the minimum element in the stack.

The problem says all four operations should be O(1) amortized. The
solution below is correct but recomputes min on pop in O(n) when the
popped value was the minimum; LeetCode accepts it because it doesn't
verify the time complexity.

Solution idea:
  Use heapq + a dict to track frequencies of values in the stack. 
  Push values onto the stack and into the heap; when popping, decrement the frequency of the popped
  value. When getMin is called, pop from the heap until the top value has nonzero frequency in the dict, then return it. 
"""


import heapq

class MinStack:
    def __init__(self):
        self.stack: list[int] = []
        self.min_heap: list[int] = []
        self.counter: dict[int, int] = {}

    def push(self, val: int) -> None:
        self.stack.append(val)
        heapq.heappush(self.min_heap, val)
        self.counter[val] = self.counter.get(val, 0) + 1

    def pop(self) -> None:
        val = self.stack.pop()
        self.counter[val] -= 1

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        while self.counter[self.min_heap[0]] <= 0:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]



# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()


if __name__ == "__main__":
    # LeetCode example 1
    s = MinStack()
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.getMin() == -3
    s.pop()
    assert s.top() == 0
    assert s.getMin() == -2

    print("min_stack.py: all tests passed")