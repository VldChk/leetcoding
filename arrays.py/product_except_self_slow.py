from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        import math
        zeroes = [0 for i in nums if i == 0]
        if len(zeroes) > 1:
            return [0] * len(nums)
        elif len(zeroes) == 1:
            non_zero = math.prod([i for i in nums if i != 0])
            return [non_zero if i == 0 else 0 for i in nums]
        
        d: dict[int, tuple[int, int]] = {}

        for n in nums:
            if n in d:
                curr = d[n][0]
                nxt = curr * n
                d[n] = (nxt, curr)
            else:
                d[n] = (n, 1)
        
        for i, n in enumerate(nums):
            pre_compute = math.prod([v[0] for k, v in d.items() if k != n])
            pre_compute *= d[n][1]
            nums[i] = pre_compute
        
        return nums
        