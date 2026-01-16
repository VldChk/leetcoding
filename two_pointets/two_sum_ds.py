import bisect


class TwoSum(object):

    def __init__(self):
        self.arr = []

    def add(self, number):
        """
        :type number: int
        :rtype: None
        """
        bisect.insort_left(self.arr, number)

    def _find_pair(self, number):
        start_idx = 0
        end_idx = len(self.arr) - 1
        while start_idx < end_idx:
            if self.arr[start_idx] + self.arr[end_idx] > number:
                end_idx -= 1
            elif self.arr[start_idx] + self.arr[end_idx] < number:
                start_idx += 1
            else:
                return True
        return False

    def find(self, value):
        """
        :type value: int
        :rtype: bool
        """
        return self._find_pair(value)


# Your TwoSum object will be instantiated and called as such:
# obj = TwoSum()
# obj.add(number)
# param_2 = obj.find(value)
