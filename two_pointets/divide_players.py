"""
LeetCode 2491 - Divide Players Into Teams of Equal Skill (Medium)
https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/

You are given a positive integer array skill of even length n where
skill[i] denotes the skill of the i-th player. Divide the players into
n / 2 teams of size 2 such that the total skill of each team is equal.

The chemistry of a team is the product of the skills of the players on
that team. Return the sum of the chemistry of all the teams, or return
-1 if there is no way to divide the players into teams such that the
total skill of each team is equal.

Solution idea:
  Sort skills. The first valid pairing — if any exists — must pair
  smallest with largest, since the only way to make every pair sum
  identical to skill[0] + skill[-1] is to keep that constant from the
  outside in. Walk two pointers from both ends: each pair must sum to
  the initial pair_val (else return -1). Sum the products as you go.
  Odd-length input is immediately impossible.
"""
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


if __name__ == "__main__":
    s = Solution()

    assert s.dividePlayers([3, 2, 5, 1, 3, 4]) == 22       # Example 1
    assert s.dividePlayers([3, 4]) == 12                   # Example 2
    assert s.dividePlayers([1, 1, 2, 3]) == -1             # Example 3

    print("divide_players.py: all tests passed")
