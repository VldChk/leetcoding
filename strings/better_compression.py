from sortedcontainers import SortedDict

class Solution:
    def betterCompression(self, compressed: str) -> str:
        sd = SortedDict()
        i = 0
        j = 1
        while j < len(compressed):
            if compressed[j].isalpha():
                if compressed[i] in sd:
                    sd[compressed[i]] += 1
                else:
                    sd[compressed[i]] = 1
                i += 1
                j += 1
            else:
                k = 0
                t = str()
                while j+k < len(compressed) and compressed[j + k].isnumeric():
                    t += compressed[j+k]
                    k += 1
                if compressed[i] in sd:
                    sd[compressed[i]] += int(t)
                else:
                    sd[compressed[i]] = int(t)
                i += (k+1)
                j += (k+1)
        res = str()
        for k, v in sd.items():
            res += k
            res += str(v)
        return res
        