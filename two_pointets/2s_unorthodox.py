from bisect import bisect, bisect_left
from typing import List
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numbers = sorted(nums)
        i = 0
        j = len(numbers) - 1
        while i < j:
            if numbers[i] + numbers[j] == target:
                idx_i = nums.index(numbers[i])
                if numbers[i] == numbers[j]:
                    idx_j = nums.index(numbers[j], idx_i+1)
                else:
                    idx_j = nums.index(numbers[j])
                return [idx_i, idx_j]
            elif numbers[i] + numbers[j] > target:
                opposite = target - numbers[i]
                idx = bisect(numbers, opposite)
                j = idx-1
            else:
                opposite = target - numbers[j]
                idx = bisect_left(numbers, opposite)
                i = idx
        return [-1, -1]