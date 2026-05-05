from bisect import bisect, bisect_left
from typing import List
class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        i = 0
        j = len(numbers) - 1
        while i < j:
            if numbers[i] + numbers[j] == target:
                return [i+1, j+1]
            elif numbers[i] + numbers[j] > target:
                opposite = target - numbers[i]
                idx = bisect(numbers, opposite)
                j = idx-1
            else:
                opposite = target - numbers[j]
                idx = bisect_left(numbers, opposite)
                i = idx
        return [-1, -1]
        
        