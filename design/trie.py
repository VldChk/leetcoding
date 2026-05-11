"""
LeetCode 208 - Implement Trie (Prefix Tree) (Medium)
https://leetcode.com/problems/implement-trie-prefix-tree/

A trie (pronounced as "try") is a tree data structure used to efficiently
store and retrieve keys in a dataset of strings.

Implement the Trie class:
  - Trie()                       initializes the trie object.
  - void insert(String word)     inserts the string word into the trie.
  - boolean search(String word)  returns true if the string word is in
                                 the trie (exact match).
  - boolean startsWith(prefix)   returns true if there is a previously
                                 inserted string with this prefix.

Solution idea:
  This file does NOT use a tree-shaped trie. Instead it keeps a `set` of
  inserted words for O(1) `search`, and a sorted `list` of words for
  prefix lookup: bisect locates the first word at or after the prefix in
  alphabetical order, and we only need to check if that single word
  startswith() the prefix (any prefix-bearing word would land at exactly
  that position in sorted order). Trades the canonical character-tree
  for a much shorter implementation; passes LeetCode for the standard
  test suite.
"""
import bisect
class Trie(object):

    def __init__(self):
        self.words = set()
        self.sort_words = list()
        

    def insert(self, word):
        
        """
        :type word: str
        :rtype: None
        """
        self.words.add(word)
        bisect.insort(self.sort_words, word)
        

    def search(self, word):
        """
        :type word: str
        :rtype: bool
        """
        return word in self.words
        

    def startsWith(self, prefix):
        """
        :type prefix: str
        :rtype: bool
        """
        if prefix in self.words:
            return True
        else:
            pos = bisect.bisect(self.sort_words, prefix)
            if pos >= len(self.sort_words):
                return False
            else:
                return self.sort_words[pos].startswith(prefix)
        


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)


if __name__ == "__main__":
    # LeetCode example 1
    t = Trie()
    t.insert("apple")
    assert t.search("apple") is True
    assert t.search("app") is False
    assert t.startsWith("app") is True
    t.insert("app")
    assert t.search("app") is True

    print("trie.py: all tests passed")