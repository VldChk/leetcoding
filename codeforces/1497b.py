"""
Codeforces 1497B - M-arrays  (Round 706, Div. 2)  [rating 1200]
https://codeforces.com/problemset/problem/1497/B

Given n positive integers and a positive integer m, distribute every
element into some arrays, reordering freely inside each one. An array is
m-divisible if every pair of adjacent elements sums to a multiple of m;
a one-element array is always m-divisible. Use as few arrays as possible.

Sample (m, a -> arrays):
  4, [2, 2, 8, 6, 9, 4]              -> 3
  8, [1, 1, 1, 5, 2, 4, 4, 8, 6, 7]  -> 6
  1, [666]                           -> 1
  2, [2, 4]                          -> 1

Solution idea:
  Only residues matter: two elements may sit next to each other exactly
  when their residues r and s satisfy r + s = 0 (mod m), so residue r
  pairs only with m - r. Each pair of classes is independent.
    - Residue 0 chains with itself, so all of it fits in one array.
    - Residue r with 2r == m (m even) also chains with itself: one array.
    - Otherwise classes r and m - r must alternate. With counts p and q,
      one array can hold 2 * min(p, q) + 1 elements when the counts
      differ, or everything when they are equal; whatever is left over
      cannot touch anything and costs one array per element. That gives
      1 array when |p - q| <= 1 and 1 + (max - min - 1) otherwise.
    - A class whose partner is absent cannot chain at all: one array each.
  The loop below realises this by draining min(p, q) from both classes,
  spending one more element on the array's odd end, and charging the
  remainder one array apiece. (In the self-pairing 2r == m case the same
  key is decremented twice and goes negative, which harmlessly collapses
  the class to the single array it deserves.) O(n) time and space.
"""
import sys
from collections import defaultdict


def solve(n: int, m: int, a_list: list[int]) -> int:
    d = defaultdict(int)

    for a in a_list:
        d[a % m] += 1

    res = 0

    for k in d:
        if k == 0:
            res += 1
            continue
        if d[k] > 0 and m - k in d and d[m - k] > 0:
            min_val = min(d[k], d[m - k])
            d[k] -= min_val
            d[m - k] -= min_val
            if d[k] > 0:
                d[k] -= 1
            elif d[m - k] > 0:
                d[m - k] -= 1
            res += 1

        if d[k] > 0:
            res += d[k]

    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, m = map(int, next(it).split())
        a_list = [int(v) for v in next(it).split()]
        out.append(str(solve(n, m, a_list)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/problemset/problem/1497/B)
        assert solve(6, 4, [2, 2, 8, 6, 9, 4]) == 3
        assert solve(10, 8, [1, 1, 1, 5, 2, 4, 4, 8, 6, 7]) == 6
        assert solve(1, 1, [666]) == 1
        assert solve(2, 2, [2, 4]) == 1
        print("1497b.py: all tests passed")
