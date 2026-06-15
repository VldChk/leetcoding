"""
Codeforces 2233C - Cost of a Bracket Sequence  (Educational Round 191)
https://codeforces.com/contest/2233/problem/C

You are given a bracket string s of length n and an integer k. Mark at
most k of its characters for removal (output '1' = removed, '0' = kept;
the number of ones must not exceed k). After the marked characters are
deleted, the cost of what remains is the length of its longest
subsequence that is a regular bracket sequence. Output any marking that
minimises this cost.

Input: t test cases; each gives n and k, then the bracket string s.
Output: a binary string of length n (the removal mask).

Solution idea:
  The cost equals 2 * (matched '(' ... ')' pairs), and a string has cost
  0 exactly when no '(' precedes a ')', i.e. it has the shape
  ")...)(...(" . For a cut point p that shape is reached by deleting the
  '(' in the prefix s[:p] and the ')' in the suffix s[p:], i.e.
  pref_open[p] + suff_close[p] deletions. Pick the cut minimising that
  count; if k is large enough remove them all (cost 0), otherwise spend
  the k removals greedily on those same characters (prefix '(' first,
  then suffix ')'), which lowers the cost as far as the budget allows.
  O(n) per test case.
"""
def solve(s, k, n):
    pref_open = [0] * (n + 1)
    for i, c in enumerate(s):
        pref_open[i + 1] = pref_open[i] + (1 if c == "(" else 0)

    suff_close = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suff_close[i] = suff_close[i + 1] + (1 if s[i] == ")" else 0)

    best = n + 1
    cut = 0

    for p in range(n + 1):
        value = pref_open[p] + suff_close[p]
        if value < best:
            best = value
            cut = p

    need = min(k, best)
    ans = ["0"] * n

    for i in range(cut):
        if need > 0 and s[i] == "(":
            ans[i] = "1"
            need -= 1

    for i in range(cut, n):
        if need > 0 and s[i] == ")":
            ans[i] = "1"
            need -= 1

    return "".join(ans)


if __name__ == "__main__":
    # Special-judged: any mask with <= k ones that reaches the minimum
    # possible cost is accepted. For each official sample, check the
    # output has length n, marks at most k characters, and reaches the
    # same cost as the known-optimal sample answer. Cost = length of the
    # longest regular-bracket subsequence of the kept characters.
    def _cost(string):
        op = match = 0
        for ch in string:
            if ch == "(":
                op += 1
            elif ch == ")" and op > 0:
                op -= 1
                match += 1
        return 2 * match

    def _kept(s, mask):
        return "".join(c for c, m in zip(s, mask) if m == "0")

    # (n, k, s, one known-optimal answer from the official samples)
    _samples = [
        (2, 1, ")(", "00"),
        (2, 0, "()", "00"),
        (4, 1, "(())", "1000"),
        (4, 1, "())(", "1000"),
        (5, 1, "((())", "00010"),
        (6, 2, "()()()", "101000"),
        (6, 2, "(()())", "001001"),
        (6, 2, "())(()", "100001"),
        (7, 3, "(()((()", "1100001"),
        (10, 3, "(()())())(", "0101001000"),
    ]
    for _n, _k, _s, _ref in _samples:
        _out = solve(_s, _k, _n)
        assert len(_out) == _n
        assert _out.count("1") <= _k
        assert _cost(_kept(_s, _out)) == _cost(_kept(_s, _ref))
    print("2233c.py: all tests passed")


if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        print(solve(s, k, n))