"""
LeetCode 49 - Group Anagrams (Medium)
https://leetcode.com/problems/group-anagrams/

Given an array of strings strs, group the anagrams together. You can
return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a
different word or phrase, typically using all the original letters
exactly once.

Solution idea:
  Two strings are anagrams iff their sorted character sequences match.
  Bucket the inputs in a dict keyed by `tuple(sorted(s))` — tuples
  are hashable so they can be dict keys, and `sorted()` runs in
  O(k log k) on a k-length word. Return the dict's values. O(n * k log k)
  overall, where n = number of strings, k = max length.
"""
from typing import List
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d: dict[tuple[str, ...], list[str]] = {}
        for s in strs:
            s_f = tuple(sorted(s))
            if s_f in d:
                d[s_f].append(s)
            else:
                d[s_f] = [s]
        return list(d.values())


if __name__ == "__main__":
    s = Solution()

    def canon(groups: list[list[str]]) -> list[list[str]]:
        return sorted([sorted(g) for g in groups])

    # Example 1
    assert canon(s.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == \
        canon([["bat"], ["nat", "tan"], ["ate", "eat", "tea"]])

    # Example 2 (single empty string)
    assert s.groupAnagrams([""]) == [[""]]

    # Example 3 (single one-char string)
    assert s.groupAnagrams(["a"]) == [["a"]]

    print("group_anagrams.py: all tests passed")
