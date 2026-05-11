"""
LeetCode 443 - String Compression (Medium)
https://leetcode.com/problems/string-compression/

Given an array of characters chars, compress it using the following
algorithm:

Begin with an empty string s. For each group of consecutive repeating
characters in chars:
  - If the group's length is 1, append the character to s.
  - Otherwise, append the character followed by the group's length.

The compressed string s should not be returned separately, but instead
be stored in the input character array chars. Note that group lengths
that are 10 or longer will be split into multiple characters in chars.

After you are done modifying the input array, return the new length of
the array. You must write an algorithm that uses only constant extra
space.

Solution idea:
  Two pointers walking the same array: `it_pos` reads, `compression_pos`
  writes. Track the previous character and a run count. When the run
  ends (next char differs), advance the writer: stamp the previous run's
  count digits (if length > 1) followed by the new character. After the
  loop, flush the final run's count if needed. Return compression_pos
  as the new length.
"""
from typing import List
class Solution:
    def compress(self, chars: List[str]) -> int:
        if len(chars) <= 1:
            return len(chars)
        it_pos: int = 1
        compression_pos: int = 1
        prev_ch = chars[0]
        cnt = 1
        while it_pos < len(chars):
            if chars[it_pos] == prev_ch:
                it_pos += 1
                cnt += 1
            else:
                prev_ch = chars[it_pos]                
                if cnt > 1:
                    s_cnt = str(cnt)
                    j: int = 0
                    while j < len(s_cnt):
                        chars[compression_pos] = s_cnt[j]
                        j += 1
                        compression_pos += 1
                chars[compression_pos] = prev_ch
                it_pos += 1
                cnt = 1
                compression_pos += 1
        s_cnt = str(cnt)
        j: int = 0
        if cnt > 1:
            while j < len(s_cnt):
                chars[compression_pos] = s_cnt[j]
                j += 1
                compression_pos += 1
        return compression_pos


if __name__ == "__main__":
    s = Solution()

    # Example 1
    chars1 = ["a", "a", "b", "b", "c", "c", "c"]
    n1 = s.compress(chars1)
    assert n1 == 6
    assert chars1[:n1] == ["a", "2", "b", "2", "c", "3"]

    # Example 2
    chars2 = ["a"]
    n2 = s.compress(chars2)
    assert n2 == 1
    assert chars2[:n2] == ["a"]

    # Example 3 (run length splits across multiple chars: "12")
    chars3 = ["a", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b", "b"]
    n3 = s.compress(chars3)
    assert n3 == 4
    assert chars3[:n3] == ["a", "b", "1", "2"]

    print("compress_string.py: all tests passed")
