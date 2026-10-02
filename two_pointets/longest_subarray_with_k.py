from typing import List
class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        if len(nums) < 2:
            return len(nums)
        freq = {}

        res = 0
        right = 0
        left = 0

        for i, val in enumerate(nums):
            right = i
            if val not in freq:
                freq[val] = 1
                continue
            elif freq[val] < k:
                freq[val] += 1
                continue
            else:
                res = max(res, right - left)
                while freq[val] == k:
                    freq[nums[left]] -= 1
                    left += 1
                freq[val] += 1
        return max(res, right - left + 1)