"""
Codeforces 2250B - String Construction  (Round 1112, Div. 2)
https://codeforces.com/contest/2250/problem/B

Given two integers n and k, construct a binary string s of length n where
both of the following hold:
  * the absolute difference between the number of '0' and the number of
    '1' in s is at most 1;
  * there are exactly k indices i (1 <= i <= n-1) with s_i = s_{i+1},
    i.e. exactly k adjacent equal pairs.
Print -1 if no such string exists. Any valid string is accepted.

Sample (n k -> one accepted answer):
  5 2 -> 01110      4 3 -> -1        6 1 -> 101001
  5 0 -> 01010      7 3 -> 0100011   4 2 -> 0011
  3 2 -> -1         7 4 -> 0111000

Solution idea:
  k = n-1 forces every character to be equal, which breaks the balance
  condition for n >= 3, and k > n-1 is impossible outright — so answer -1
  exactly when k >= n-1. Otherwise build a core of (k//2 + 1) ones
  followed by (k - k//2 + 1) zeros: it has length k+2 and contributes
  exactly k adjacent equal pairs, with the 1->0 junction contributing
  none. Pad the remaining n-k-2 characters with a strictly alternating
  tail starting at '1', which adds no further pairs and evens out the
  counts. O(n) time and space.
"""
import sys


def solve(n, k):
    def _construct(cnt, first_is_zero=True):
        if cnt <= 0:
            return ""

        res = str()
        for i in range(cnt):
            if first_is_zero:
                res += "0" if i % 2 == 0 else "1"
            else:
                res += "1" if i % 2 == 0 else "0"
        return res
    if k >= n-1:
        return -1

    core = "1" * (k // 2 + 1) + "0" * (k - k // 2 + 1)
    return core + _construct(n - len(core), first_is_zero=False)


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, k = (int(v) for v in next(it).split())
        out.append(str(solve(n, k)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        def _ok(s, n, k):
            return (len(s) == n
                    and abs(s.count('0') - s.count('1')) <= 1
                    and sum(1 for i in range(n - 1) if s[i] == s[i + 1]) == k)

        # Official samples (codeforces.com/contest/2250/problem/B). Any valid
        # string is accepted, so check the two properties, not the exact text.
        assert _ok(solve(5, 2), 5, 2)
        assert solve(4, 3) == -1
        assert _ok(solve(6, 1), 6, 1)
        assert _ok(solve(5, 0), 5, 0)
        assert _ok(solve(7, 3), 7, 3)
        assert _ok(solve(4, 2), 4, 2)
        assert solve(3, 2) == -1
        assert _ok(solve(7, 4), 7, 4)
        print("2250b.py: all tests passed")
