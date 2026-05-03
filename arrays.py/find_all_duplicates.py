
from typing import List
class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        i = 0
        dups: List[int] = []
        nums = [i-1 for i in nums]
        for i, n in enumerate(nums):
            if n == i:
                continue
            else:
                nums[i] = -1
                t = n
                while True:
                    if nums[t] == t:
                        dups.append(t)
                        break
                    else:
                        nums[t], t = t, nums[t]
                        if t == -1:
                            break

        return [d+1 for d in dups]
