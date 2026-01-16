from typing import List
class Solution:
    def numRabbits(self, answers: List[int]) -> int:
        d = {}
        res = 0
        for answer in answers:
            if answer in d:
                d[answer] -= 1
                if d[answer] == 0:
                    res += answer + 1
                    d[answer] = answer + 1
            else:
                d[answer] = answer + 1
        for k in d.keys():
            res += k + 1
        
        return res