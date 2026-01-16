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