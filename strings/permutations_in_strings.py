from collections import Counter

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) == len(s2):
            s1_c = Counter(s1)
            s2_c = Counter(s2)
            return s1_c == s2_c
        elif len(s1) < len(s2):
            s1_c = dict(Counter(s1))
        else:
            return False

        k = len(s1)

        big_c = dict(Counter(s2[:k]))

        for i in range(k, len(s2)):
            if big_c == s1_c:
                return True
            else:
                big_c[s2[i-k]] -= 1
                if big_c[s2[i-k]] == 0:
                    del big_c[s2[i-k]]
                big_c[s2[i]] = big_c.get(s2[i], 0) + 1
        
        return big_c == s1_c

        
        
        