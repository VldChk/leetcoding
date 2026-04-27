class MinStack:

    def __init__(self):
        self.stack = []
        self.__min = None
        

    def push(self, val: int) -> None:
        self.stack.append(val)
        if self.__min is None or val < self.__min:
            self.__min = val

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.__min:
            try:
                self.__min = min(self.stack)
            except ValueError:
                self.__min = None
        

    def top(self) -> int:
        return self.stack[-1]
        

    def getMin(self) -> int:
        return self.__min
        


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()