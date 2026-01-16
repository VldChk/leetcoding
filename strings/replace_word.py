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
