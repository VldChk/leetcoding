from typing import List
class Solution:
    def expand(self, s: str) -> List[str]:
        i = 0
        res: List[str] = [""]
        while i < len(s):
            if s[i] != "{":
                res = [r + s[i] for r in res]
            else:
                i += 1
                options: List[str] = []
                while s[i] != "}":
                    if s[i] == ",":
                        i += 1
                        continue
                    options.append(s[i])
                    i += 1
                options.sort()
                res = [r + o for r in res for o in options]
            i += 1
        return res