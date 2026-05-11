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
  Sliding window over per-index costs. Maintain a deque of costs in the
  current window plus a running sum `curr_s`. For each new index push
  its cost into the window; while the window total exceeds maxCost,
  pop from the left to shrink it. The window length after shrinking is
  always feasible; track its maximum across the scan. This is the
  canonical O(n) two-pointer solution and correctly enforces the
  contiguous-substring constraint.
"""


class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        from collections import deque
        s = s.lower()
        t = t.lower()
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        counter = 0
        max_counter = 0
        q = deque([])
        curr_s = 0
        for i in range(len(s)):
            cost = abs(alphabet.index(s[i]) - alphabet.index(t[i]))
            q.append(cost)
            curr_s += cost
            while q and curr_s > maxCost:
                curr_s -= q.popleft()
                counter -= 1
            counter = len(q)
            max_counter = max(max_counter, counter)
        return max(max_counter, counter)


if __name__ == "__main__":
    s = Solution()

    assert s.equalSubstring("abcd", "bcdf", 3) == 3       # Example 1
    assert s.equalSubstring("abcd", "cdef", 3) == 1       # Example 2
    assert s.equalSubstring("abcd", "acde", 0) == 1       # Example 3

    print("budget_substring_replace.py: all tests passed")