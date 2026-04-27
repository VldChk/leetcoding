from typing import List
class Solution:
    def findPairs(self, nums: List[int], k: int) -> int:
        nums.sort()
        if len(nums) < 2:
            return 0
        i = 0
        j = 1
        cnt = 0
        while i < j and j < len(nums):
            if abs(nums[i] - nums[j]) == k:
                cnt += 1
                while i+1 < j and nums[i+1] == nums[i]:
                    i += 1
                while j+1 < len(nums) and nums[j+1] == nums[j]:
                    j += 1
                j += 1
            elif abs(nums[i] - nums[j]) < k:
                j += 1
            else:
                i += 1
            if i == j:
                j += 1
        return cnt
        