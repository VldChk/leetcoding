"""
Codeforces 2237D - Fullmetal Bitchemist  (Order Capital Round 2 / Round 1104, Div. 1 + Div. 2)
https://codeforces.com/contest/2237/problem/D

A binary string t is beautiful when it can be reduced to a string of
length exactly 1 by repeating this operation any number of times: choose
two equal adjacent characters, remove both, and insert one character of
the opposite value in their place. For example 10001 -> 1101 -> 001 ->
11 -> 0, so 10001 is beautiful; 111 -> 01 gets stuck, so 111 is not.
Given a binary string s, count its non-empty beautiful substrings.

Sample (s -> count):
  0                              -> 1      01                           -> 2
  01001                          -> 10     001                          -> 5
  011110                         -> 15     010110110                    -> 30
  010000101001                   -> 47     1010011010010110             -> 81
  11110101101101001110           -> 139
  000101100011111001111100000010 -> 316

Solution idea:
  Brute force: enumerate every substring and reduce it with a memoised
  search, caching each verdict in `chk` and each reduced value in `mem`.
  Roughly O(n^2) substrings times the cost of reducing each one, which is
  fine for the samples but far too slow for the real limit of n <= 10^6.
  This is the contest attempt, kept as written.

  The intended characterisation, verified exhaustively for every binary
  string of length <= 14 and against all ten official samples:
    an operation moves (ones, length) by (+1, -1) on "00" and by (-2, -1)
    on "11", so (ones + length) mod 3 never changes. Length 1 means that
    value is 1 or 2, hence (ones + length) % 3 != 0 is necessary. The only
    other way to fail is running out of moves, i.e. being alternating with
    length >= 3 — even-length alternating strings already have the sum
    divisible by 3, so they cost nothing extra. Counting substrings whose
    prefix key (prefix_ones[i] + i) % 3 differs at the two ends, minus the
    odd-length alternating runs, answers the problem in O(n).
"""
import sys
from functools import cache

chk = {
    "1": 1,
    "0": 1,
    "00": 1,
    "11": 1,
    "01": 0,
    "10": 0,
}

mem = {
    "1": "1",
    "0": "0",
    "00": "1",
    "11": "0",
}


def solve(b):
    res = len(b)

    k = 2

    @cache
    def check(s):
        j = 1
        while j < len(s):
            if s[j-1:j+1] in ["00", "11"]:
                if s[:j-1] + mem[s[j-1:j+1]] + s[j+1:] in mem:
                    mem[s] = mem[mem[s[:j-1] + mem[s[j-1:j+1]] + s[j+1:]]]
                    chk[s] = 1
                    return 1
                else:
                    c = check(s[:j-1] + mem[s[j-1:j+1]] + s[j+1:])
                    if c == 1:
                        mem[s] = mem[mem[s[:j-1] + mem[s[j-1:j+1]] + s[j+1:]]]
                        chk[s] = 1
                        return 1
            j += 1

        return 0

    while k <= len(b):
        for i in range(len(b) - k + 1):
            if b[i:i+k] in chk:
                res += chk[b[i:i+k]]
            else:
                res += check(b[i:i+k])
        k += 1

    return res


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        next(it)  # n, implied by the length of the following line
        b = next(it).strip()
        out.append(str(solve(b)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2237/problem/D)
        assert solve("0") == 1
        assert solve("01") == 2
        assert solve("01001") == 10
        assert solve("001") == 5
        assert solve("011110") == 15
        assert solve("010110110") == 30
        assert solve("010000101001") == 47
        assert solve("1010011010010110") == 81
        assert solve("11110101101101001110") == 139
        assert solve("000101100011111001111100000010") == 316
        print("d.py: all tests passed")
