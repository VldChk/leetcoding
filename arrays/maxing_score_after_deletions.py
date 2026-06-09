"""
LeetCode 3496 — Maximize Score After Pair Deletions (Medium)
https://leetcode.com/problems/maximize-score-after-pair-deletions/

While `len(nums) > 2`, repeatedly perform ONE of:
    (a) remove the first TWO elements,
    (b) remove the last TWO elements,
    (c) remove the FIRST and LAST element.
Each removal adds the sum of removed values to your score. Return the maximum
score achievable.

Examples:
    [2, 3, 2]         -> 5   (len already <= 3 odd: keep min, remove rest)
    [1, 2]            -> 0   (length 2: no operation possible)
    [5, 4, 3, 2]      -> 9   (even: remove worst adjacent pair (3,2)=5, score=14-5)

Idea — what is FORCED to remain:
Each operation removes 2 elements at a time, so the parity of length is
preserved. Starting from length n:
    - n odd  -> stops at length 1: exactly one element survives.
    - n even -> stops at length 2: exactly two elements survive.
Operations (a), (b), (c) can leave ANY single element behind (odd case) or
ANY adjacent pair behind (even case — c shrinks from the ends until two
adjacent elements remain). So:
    max_score = total_sum - min(remainder),
    where remainder = min(nums) if n odd, else min over adjacent-pair sums.

Complexity:
    Time  O(n)
    Space O(1)
"""
from typing import List
from itertools import pairwise

class Solution:
    def maxScore(self, nums: List[int]) -> int:
        if len(nums) < 3:
            return 0

        if len(nums) % 2 == 0:
            curr_min = min(map(sum, pairwise(nums)))
            return sum(nums) - curr_min
        else:
            curr_min = min(nums)
            return sum(nums) - curr_min


if __name__ == "__main__":
    sol = Solution()

    # Example 1 (official LC sample) — odd length, smallest single element = 2
    assert sol.maxScore([2, 3, 2]) == 5
    # Example 2 (official LC sample) — length 2, no operations possible
    assert sol.maxScore([1, 2]) == 0
    # Even length: drop the worst adjacent pair (3,2)=5 -> 14-5=9
    assert sol.maxScore([5, 4, 3, 2]) == 9
    # Even length, worst adjacent pair is at the front: (1,2)=3 -> 24-3=21
    assert sol.maxScore([1, 2, 9, 8, 4]) == sum([1, 2, 9, 8, 4]) - min(1, 9)
    # Single element — no operation possible
    assert sol.maxScore([7]) == 0
    # Length 2 — no operation possible
    assert sol.maxScore([100, 200]) == 0
    # Length 3 odd — remove the minimum
    assert sol.maxScore([10, 1, 5]) == 15
    print("maxing_score_after_deletions.py: all tests passed")
