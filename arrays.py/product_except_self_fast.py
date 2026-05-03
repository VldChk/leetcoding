
from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        res = [1] * len(nums)
        for i in range(1, len(nums)):
            res[i] = res[i-1] * nums[i-1]
        
        right_cumulative = 1
        for j in range(len(nums)-1, -1, -1):
            res[j] = res[j] * right_cumulative
            right_cumulative = right_cumulative * nums[j]
        
        return res