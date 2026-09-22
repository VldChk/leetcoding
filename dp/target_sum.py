from typing import List

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        memo = {}
        def _dfs(prev_val: int, curr_idx: int) -> int:
            if (prev_val, curr_idx) in memo:
                return memo[(prev_val, curr_idx)]
            
            positive = prev_val + nums[curr_idx]
            negative = prev_val - nums[curr_idx]
            if curr_idx == len(nums) - 1:
                cnt = (positive == target) + (negative == target)
            else:
                cnt = _dfs(positive, curr_idx + 1) + _dfs(negative, curr_idx + 1)
            
            memo[(prev_val, curr_idx)] = cnt
            return cnt
        return _dfs(0, 0)