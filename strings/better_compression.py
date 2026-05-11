"""
LeetCode 3167 - Better Compression of String (Medium)
https://leetcode.com/problems/better-compression-of-string/

You are given a string compressed representing a compressed version of a
string. The format is a character followed by its frequency (e.g.,
"a3b1a1c2" decompresses to "aaabacc"). The frequencies are positive
integers (no leading zeros, no zero frequency).

Return the "better" compression where each distinct character appears
exactly once, listed in alphabetical order, with the combined total
frequency.

Solution idea:
  Walk the input with two cursors (i = letter slot, j = scan head into
  digit run). Each step locates the digit run after position i, parses
  the integer, accumulates it into a SortedDict keyed by the letter.
  At the end, iterate the SortedDict (already alphabetical) and emit
  letter + str(count).
"""
from sortedcontainers import SortedDict

class Solution:
    def betterCompression(self, compressed: str) -> str:
        sd = SortedDict()
        i = 0
        j = 1
        while j < len(compressed):
            if compressed[j].isalpha():
                if compressed[i] in sd:
                    sd[compressed[i]] += 1
                else:
                    sd[compressed[i]] = 1
                i += 1
                j += 1
            else:
                k = 0
                t = str()
                while j+k < len(compressed) and compressed[j + k].isnumeric():
                    t += compressed[j+k]
                    k += 1
                if compressed[i] in sd:
                    sd[compressed[i]] += int(t)
                else:
                    sd[compressed[i]] = int(t)
                i += (k+1)
                j += (k+1)
        res = str()
        for k, v in sd.items():
            res += k
            res += str(v)
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.betterCompression("a3c9b2c1") == "a3b2c10"   # Example 1
    assert s.betterCompression("c2b3a1") == "a1b3c2"      # Example 2
    assert s.betterCompression("a2b4c1") == "a2b4c1"      # Example 3

    print("better_compression.py: all tests passed")
