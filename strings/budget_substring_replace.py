class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        from collections import deque
        s = s.lower()
        t = t.lower()
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        counter = 0
        max_counter = 0
        q = deque([])
        curr_s = 0
        for i in range(len(s)):
            cost = abs(alphabet.index(s[i]) - alphabet.index(t[i]))
            q.append(cost)
            curr_s += cost
            while q and curr_s > maxCost:
                curr_s -= q.popleft()
                counter -= 1
            counter = len(q)
            max_counter = max(max_counter, counter)
        return max(max_counter, counter)