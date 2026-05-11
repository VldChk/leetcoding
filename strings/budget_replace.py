"""
LeetCode 1208 - Get Equal Substrings Within Budget (Medium)
https://leetcode.com/problems/get-equal-substrings-within-budget/

You are given two strings s and t of the same length and an integer
maxCost. Changing the i-th character of s to the i-th character of t
costs |s[i] - t[i]| (absolute difference of ASCII values).

Return the maximum length of a substring of s that can be changed to
the corresponding substring of t with a total cost less than or equal
to maxCost. If there is no such substring, return 0.

Solution idea (this file's approach):
  Group all per-position costs into a dict cost -> [indices], walk costs
  ascending and greedily count how many positions you can "afford" with
  the budget. Note: this greedy "any positions" interpretation does NOT
  enforce the substring being contiguous, so it does not solve LC 1208
  in general. It happens to give the correct answer on LeetCode's three
  published examples (where costs are uniform or near-uniform). The
  sibling file `budget_substring_replace.py` contains a correct sliding-
  window solution. Tests below mirror the LC examples and pass on this
  implementation.
"""


class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        s = s.lower()
        t = t.lower()
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        cost_map = {}
        for i in range(len(s)):
            _t1 = alphabet.index(t[i])
            _t2 = alphabet.index(s[i])
            cost = abs(alphabet.index(s[i]) - alphabet.index(t[i]))
            if cost in cost_map:
                cost_map[cost].append(i)
            else:
                cost_map[cost] = [i]
        cost_map = {k: cost_map[k] for k in sorted(cost_map.keys())}
        budget = maxCost
        counter = 0
        for k, v in cost_map.items():
            idx = 0
            while k <= budget and idx < len(v):
                counter += 1
                budget -= k
                idx += 1
            if k > budget:
                break
        return counter


if __name__ == "__main__":
    s = Solution()

    assert s.equalSubstring("abcd", "bcdf", 3) == 3       # Example 1
    assert s.equalSubstring("abcd", "cdef", 3) == 1       # Example 2
    assert s.equalSubstring("abcd", "acde", 0) == 1       # Example 3

    print("budget_replace.py: all tests passed")