"""
LeetCode 648 - Replace Words (Medium)
https://leetcode.com/problems/replace-words/

In English, we have a concept called root, which can be followed by
some other word to form another longer word - let's call this word
derivative. For example, when the root "help" is followed by the word
"ful", we can form a derivative "helpful".

Given a dictionary consisting of many roots and a sentence consisting
of words separated by spaces, replace all the derivatives in the
sentence with the root forming it. If a derivative can be replaced by
more than one root, replace it with the root that has the shortest
length. Return the sentence after replacement.

Solution idea (sorted-list "trie" replacement):
  Build a sorted list `trie` of dictionary roots, dropping any root that
  is a derivative of an already-stored shorter root, and trimming any
  longer roots that the new (shorter) root subsumes. For each sentence
  word, bisect_left into the trie and look at the immediately preceding
  entry — if the word starts with that entry, replace; otherwise leave.
  This works because in sorted order any shorter root is a prefix of all
  derivatives that follow alphabetically, so the predecessor is the
  shortest root that could match.
"""
from typing import List
import bisect

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        trie = []
        for prefix in dictionary:
            idx = bisect.bisect_left(trie, prefix)
            if idx-1 >= 0 and idx-1 < len(trie) and prefix.startswith(trie[idx-1]):
                continue
            if idx >= 0 and idx < len(trie) and trie[idx].startswith(prefix):
                trie[idx] = prefix
                while idx+1 < len(trie) and trie[idx+1].startswith(prefix):
                    del trie[idx+1]
            else:
                bisect.insort(trie, prefix)
        res = []
        for word in sentence.strip().split(" "):
            idx = bisect.bisect_left(trie, word) - 1
            if idx < len(trie) and word.startswith(trie[idx]):
                res.append(trie[idx])
            else:
                res.append(word)
        return " ".join(res)


if __name__ == "__main__":
    s = Solution()

    assert s.replaceWords(
        ["cat", "bat", "rat"],
        "the cattle was rattled by the battery"
    ) == "the cat was rat by the bat"                          # Example 1

    assert s.replaceWords(
        ["a", "b", "c"],
        "aadsfasf absbs bbab cadsfafs"
    ) == "a a b c"                                              # Example 2

    print("replace_word.py: all tests passed")
