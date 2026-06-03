"""
LeetCode 609 — Find Duplicate File in System (Medium)
https://leetcode.com/problems/find-duplicate-file-in-system/

Given a list of directory-info strings, return groups of files that share the
same content. Each input has the format:
    "root/d1/d2/.../dm f1.txt(content1) f2.txt(content2) ..."
The first whitespace-separated token is the directory path; every remaining
token is `filename(content)`. Return groups (any order) where each group has
2+ file paths whose contents collide.

Example:
    paths = ["root/a 1.txt(abcd) 2.txt(efgh)",
             "root/c 3.txt(abcd)",
             "root/c/d 4.txt(efgh)",
             "root 4.txt(efgh)"]
    -> [["root/a/2.txt","root/c/d/4.txt","root/4.txt"],
        ["root/a/1.txt","root/c/3.txt"]]

Idea — invert into a content→[paths] dict:
For each directory entry, split off the directory, then split each file token at
'(' to separate name from content. Use content as the dict key and accumulate
full paths as values. Final answer is the list of values with length > 1.

Complexity:
    Time  O(N) over total input length
    Space O(N) for the dict
"""
from itertools import islice
from typing import List
class Solution:
    def findDuplicate(self, paths: List[str]) -> List[List[str]]:
        mem = {}
        for path in paths:
            try:
                parts = path.split(" ")
                dir = parts[0]
                for files in islice(parts, 1, None):
                    fl, content = files.split("(")
                    hsh = content.replace(")", "").strip().lower()
                    if hsh in mem:
                        mem[hsh].append(dir + "/" + fl)
                    else:
                        mem[hsh] = [dir + "/" + fl]
            except:
                continue
        return [v for v in mem.values() if len(v) > 1]


if __name__ == "__main__":
    def canon(groups):
        """Order-insensitive comparison: sort within each group, then sort outer."""
        return sorted(sorted(g) for g in groups)

    sol = Solution()

    paths = [
        "root/a 1.txt(abcd) 2.txt(efgh)",
        "root/c 3.txt(abcd)",
        "root/c/d 4.txt(efgh)",
        "root 4.txt(efgh)",
    ]
    expected = [
        ["root/a/2.txt", "root/c/d/4.txt", "root/4.txt"],
        ["root/a/1.txt", "root/c/3.txt"],
    ]
    assert canon(sol.findDuplicate(paths)) == canon(expected)

    # No duplicates at all -> empty result
    assert sol.findDuplicate(["root/a 1.txt(abc) 2.txt(def)"]) == []

    # Three-way duplicate
    paths2 = [
        "root/a 1.txt(xx)",
        "root/b 2.txt(xx)",
        "root/c 3.txt(xx)",
    ]
    assert canon(sol.findDuplicate(paths2)) == canon(
        [["root/a/1.txt", "root/b/2.txt", "root/c/3.txt"]]
    )
    print("find_duplicative_files.py: all tests passed")