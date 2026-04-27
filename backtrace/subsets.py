from typing import List


class Solution:

    def subsets(self, nums: List[int]) -> List[List[int]]:
        def _backtrace(it: List[int], nums: List[int], res: List[List[int]]):
            for i in range(len(nums)):
                t = it + [nums[i]]
                res.append(t)
                if i == len(nums) - 1:
                    return
                _backtrace(t, nums[i + 1 :], res)
            return res

        res = [[]]
        it = []
        i = 2
        _backtrace(it, nums, res)
        return res
