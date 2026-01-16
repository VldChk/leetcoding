from typing import List

class Solution:
    def dividePlayers(self, skill: List[int]) -> int:
        if len(skill) % 2 == 1:
            return -1
        skill.sort()
        i = 0
        j = len(skill) - 1
        pair_val = skill[0] + skill[-1]
        res = 0

        while i < j:
            if skill[i] + skill[j] == pair_val:
                res += skill[i] * skill[j]
                i += 1
                j -= 1
            else:
                return -1
        return res
        