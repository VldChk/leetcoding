"""
LeetCode 760 - Find Anagram Mappings (Easy, Premium)
https://leetcode.com/problems/find-anagram-mappings/

You are given two integer arrays nums1 and nums2 where nums2 is an
anagram of nums1 (nums2 is built by randomly reordering the elements of
nums1). Return an index mapping array `mapping` such that mapping[i] = j
means the i-th element of nums1 appears at index j in nums2. The arrays
may contain duplicates; if several valid answers exist, return any.

Example:
  nums1 = [12, 28, 46, 32, 50], nums2 = [50, 12, 32, 46, 28]
  -> [1, 4, 3, 2, 0]   (nums1[0]=12 sits at nums2[1], and so on)

Solution idea:
  Build a hash map value -> index from nums2 (for duplicate values the
  last index wins, which is still a valid answer), then look up every
  value of nums1 in order. O(n) time, O(n) space.
"""
from typing import List
class Solution:
    def anagramMappings(self, nums1: List[int], nums2: List[int]) -> List[int]:
        d = {}
        for i, n in enumerate(nums2):
            d[n] = i
        res = []
        for j, n in enumerate(nums1):
            res.append(d[n])
        return res


if __name__ == "__main__":
    s = Solution()

    # Official example
    assert s.anagramMappings([12, 28, 46, 32, 50], [50, 12, 32, 46, 28]) == [1, 4, 3, 2, 0]
    # Single element / already aligned
    assert s.anagramMappings([1], [1]) == [0]
    assert s.anagramMappings([5, 6, 7], [5, 6, 7]) == [0, 1, 2]

    print("anagram_mapping.py: all tests passed")
