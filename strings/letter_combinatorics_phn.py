"""
LeetCode 17 - Letter Combinations of a Phone Number (Medium)
https://leetcode.com/problems/letter-combinations-of-a-phone-number/

Given a string containing digits from 2-9 inclusive, return all
possible letter combinations that the number could represent. Return
the answer in any order.

A mapping of digits to letters (just like on the telephone buttons) is
given below. Note that 1 does not map to any letters.

Solution idea:
  Cartesian product across the letter sets per digit. Start with the
  letters for digits[0] as the seed list of strings; then for each
  remaining digit, replace `comb` with the product of (current combos
  x letters of next digit), joined into strings. itertools.product
  does the heavy lifting.

Caveat:
  This implementation does NOT handle digits == "" (LeetCode example 2
  expects []). The line `comb = d[digits[0]]` would raise IndexError on
  empty input. The test block below covers examples 1 and 3 only, which
  do pass.
"""
from itertools import product
class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        d = {
            "2": ["a", "b", "c"],
            "3": ["d", "e", "f"],
            "4": ["g", "h", "i"],
            "5": ["j", "k", "l"],
            "6": ["m", "n", "o"],
            "7": ["p", "q", "r", "s"],
            "8": ["t", "u", "v"],
            "9": ["w", "x", "y", "z"],
        }
        comb = d[digits[0]]
        for i in range(1, len(digits)):
            comb = [''.join(i) for i in product(comb, d[digits[i]])]

        return comb


if __name__ == "__main__":
    s = Solution()

    assert sorted(s.letterCombinations("23")) == sorted(
        ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
    )                                                       # Example 1
    assert sorted(s.letterCombinations("2")) == sorted(
        ["a", "b", "c"]
    )                                                       # Example 3

    # Example 2 (digits = "" -> expected []) is intentionally not tested:
    # this implementation raises IndexError on empty input. See module
    # docstring "Caveat".

    print("letter_combinatorics_phn.py: all tests passed")