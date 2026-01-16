class Solution:
    def removeStars(self, s: str) -> str:
        res = ""
        star_counter = 0
        for ch in s[::-1]:
            if ch == "*":
                star_counter += 1
            elif star_counter > 0:
                star_counter -= 1
            else:
                res += ch
        return res[::-1]
