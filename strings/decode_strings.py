class Solution:
    def decodeString(self, s: str) -> str:
        def _recursive_parsing(s: str, i: int) -> tuple[str, int]:
            res: str = ""
            num = 0
            while s[i].isnumeric():
                num = (num*10) + int(s[i])
                i += 1
            i += 1
            while s[i] != "]":
                if s[i].isnumeric():
                    t, i = _recursive_parsing(s, i)
                    res += t
                else:
                    res += s[i]
                    i += 1
           
            i += 1
            
            return res * num, i
        
        j = 0
        res: str = ""
        while j < len(s):
            if s[j].isnumeric():
                t, j = _recursive_parsing(s, j)
                res += t
            else:
                res += s[j]
                j += 1
        
        return res
            
