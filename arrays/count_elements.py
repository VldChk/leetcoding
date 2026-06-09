"""
LeetCode 1426 — Counting Elements (Easy, Premium)
https://leetcode.com/problems/counting-elements/

Given an integer array `arr`, count the elements `x` such that `x + 1` is also
in `arr`. Each duplicate of `x` counts independently — if `arr = [1,1,2]`, both
1s count, so the answer is 2 (not 1).

Examples:
    [1,2,3]               -> 2   (1 and 2 each have +1 in the array)
    [1,1,3,3,5,5,7,7]     -> 0   (no x where x+1 is present)
    [1,3,2,3,5,0]         -> 3   (0, 1, 2 each appear once and have x+1 present)
    [1,1,2,2]             -> 2   (both 1s qualify; 2s do not — no 3 in array)

Idea — frequency map + sum-of-counts:
Count occurrences with a dict. Iterate keys; whenever `x + 1` is also a key,
add the *count* of `x` (not just 1) to the result. Hash-set lookup keeps the
membership test O(1).

Complexity:
    Time  O(n)
    Space O(n) for the dict
"""
from typing import List
class Solution:
    def countElements(self, arr: List[int]) -> int:
        d = {}
        for el in arr:
            d[el] = d.get(el, 0) + 1
        
        res = 0

        for el, cnt in d.items():
            if el + 1 in d:
                res += cnt

        return res


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    assert sol.countElements([1, 2, 3]) == 2
    # Example 2 — no x has x+1 in arr
    assert sol.countElements([1, 1, 3, 3, 5, 5, 7, 7]) == 0
    # Example 3 — 0/1/2 each have a successor
    assert sol.countElements([1, 3, 2, 3, 5, 0]) == 3
    # Duplicates count individually
    assert sol.countElements([1, 1, 2, 2]) == 2
    # Single element — no successor possible
    assert sol.countElements([5]) == 0
    # All same
    assert sol.countElements([4, 4, 4]) == 0
    print("count_elements.py: all tests passed")
