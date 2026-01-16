class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        s = s.lower()
        t = t.lower()
        alphabet = list('abcdefghijklmnopqrstuvwxyz')
        cost_map = {}
        for i in range(len(s)):
            _t1 = alphabet.index(t[i])
            _t2 = alphabet.index(s[i])
            cost = abs(alphabet.index(s[i]) - alphabet.index(t[i]))
            if cost in cost_map:
                cost_map[cost].append(i)
            else:
                cost_map[cost] = [i]
        cost_map = {k: cost_map[k] for k in sorted(cost_map.keys())}
        budget = maxCost
        counter = 0
        for k, v in cost_map.items():
            idx = 0
            while k <= budget and idx < len(v):
                counter += 1
                budget -= k
                idx += 1
            if k > budget:
                break
        return counter