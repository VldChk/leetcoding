from typing import List

class Solution:
    def findOcurrences(self, text: str, first: str, second: str) -> List[str]:
        if len(text.split(" ")) < 3:
            return []
        res = []
        minus_two = ""
        minus_one = ""
        for i, word in enumerate(text.split(" ")):
            if i < 2:
                minus_two = minus_one
                minus_one = word
                continue  # somehow, start= not always work and I am lazy to debug
            if minus_two == first and minus_one == second:
                res.append(word)

            minus_two = minus_one
            minus_one = word
        return res
