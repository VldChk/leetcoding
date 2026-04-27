class Solution:
    def isHappy(self, n: int) -> bool:
        def _recur(n: int) -> bool:
            r = 0
            i = n
            while i > 0:
                r += (i % 10) ** 2
                i = i // 10
            if r == 1:
                return True
            elif r in mem:
                return False
            else:
                mem.add(r)
                return _recur(r)

        mem = set()
        return _recur(n)
