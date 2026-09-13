"""
Codeforces 1512C - A-B Palindrome  (Round 713, Div. 3)
https://codeforces.com/problemset/problem/1512/C

You are given a string s of '0', '1' and '?', and two integers a and b.
Replace every '?' with '0' or '1' so that s becomes a palindrome holding
exactly a characters '0' and exactly b characters '1'. Print the result,
or -1 if it cannot be done. Any valid result is accepted.

Sample (a b s -> one accepted answer):
  4 4 01?????0 -> 01011010      3 3 ??????  -> -1
  1 0 ?        -> 0             2 2 0101    -> -1
  2 2 01?0     -> 0110          0 1 0       -> -1
  0 3 1?1      -> 111           2 2 ?00?    -> 1001
  4 3 ??010?0  -> 0101010

Solution idea:
  A palindrome's characters come in mirrored pairs, plus a single middle
  character when the length is odd, so at most one of a and b may be odd,
  only when the length is odd, and the middle must take that character.
  First pass over the pairs: copy a fixed character onto its '?' mirror,
  reject two different fixed characters, and subtract every settled pair
  from the counts. Second pass: fill each fully unknown pair with
  whichever character has more remaining. The result is valid exactly
  when both counts land on zero. O(n) time and space.
"""
import sys


def solve(s, a, b):
    if a % 2 == 1 and b % 2 == 1:
        return "-1"

    if len(s) != a + b:
        return "-1"

    if len(s) % 2 == 1 and a % 2 == 0 and b % 2 == 0:
        return "-1"

    if len(s) % 2 == 0 and (a % 2 == 1 or b % 2 == 1):
        return "-1"

    if len(s) % 2 == 1:
        if a % 2 == 1 and s[len(s)//2] == '1':
            return "-1"
        if b % 2 == 1 and s[len(s)//2] == '0':
            return "-1"
        if a % 2 == 1:
            s[len(s)//2] = '0'
            a -= 1
        if b % 2 == 1:
            s[len(s)//2] = '1'
            b -= 1

    mid_idx = len(s) // 2

    k = 0

    while k < mid_idx:
        if s[k] == '?' and s[-(k+1)] != '?':
            s[k] = s[-(k+1)]
            if s[k] == '0':
                a -= 2
            else:
                b -= 2
        elif s[k] != '?' and s[-(k+1)] == '?':
            s[-(k+1)] = s[k]
            if s[k] == '0':
                a -= 2
            else:
                b -= 2
        elif s[k] != '?' and s[-(k+1)] != '?' and s[k] != s[-(k+1)]:
            return "-1"
        elif s[k] == '0' and s[-(k+1)] == '0':
            a -= 2
        elif s[k] == '1' and s[-(k+1)] == '1':
            b -= 2

        k += 1

    k = 0

    while k < mid_idx:
        if s[k] == '?' and s[-(k+1)] == '?':
            if a >= b:
                s[k] = s[-(k+1)] = '0'
                a -= 2
            else:
                s[k] = s[-(k+1)] = '1'
                b -= 2
        k += 1

    if a != 0 or b != 0:
        return "-1"

    return "".join(s)


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        a, b = (int(v) for v in next(it).split())
        s = list(next(it).strip())
        out.append(solve(s, a, b))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        def _ok(res, a, b, s):
            return (len(res) == len(s) and res == res[::-1]
                    and res.count('0') == a and res.count('1') == b
                    and all(c == '?' or c == r for c, r in zip(s, res)))

        # Official samples (codeforces.com/problemset/problem/1512/C). Any valid
        # palindrome is accepted, so check its properties, not the exact text.
        # solve() fills its list argument in place, so pass a fresh list.
        assert _ok(solve(list("01?????0"), 4, 4), 4, 4, "01?????0")
        assert solve(list("??????"), 3, 3) == "-1"
        assert _ok(solve(list("?"), 1, 0), 1, 0, "?")
        assert solve(list("0101"), 2, 2) == "-1"
        assert _ok(solve(list("01?0"), 2, 2), 2, 2, "01?0")
        assert solve(list("0"), 0, 1) == "-1"
        assert _ok(solve(list("1?1"), 0, 3), 0, 3, "1?1")
        assert _ok(solve(list("?00?"), 2, 2), 2, 2, "?00?")
        assert _ok(solve(list("??010?0"), 4, 3), 4, 3, "??010?0")
        print("1512C.py: all tests passed")
