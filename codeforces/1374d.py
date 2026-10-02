"""
Codeforces 1374D - Zero Remainder Array  (Round 653, Div. 3)  [rating 1400]
https://codeforces.com/problemset/problem/1374/D

Start with x = 0. Each move is either "pick an index i and do a_i += x,
then x += 1" or just "x += 1". The adding form may be used at most once
per index. Find the minimum number of moves after which every element is
divisible by k. (The divisor is called k in the statement; the code below
names it m.)

Sample (k, a -> moves):
  3,  [1, 2, 1, 3]                     -> 6
  6,  [8, 7, 1, 8, 3, 7, 5, 10, 8, 9]  -> 18
  10, [20, 100, 50, 20, 100500]        -> 0
  25, [24] * 10                        -> 227
  8,  [1, 2, 3, 4, 5, 6, 7, 8]         -> 8

Solution idea:
  An element with a_i % m == r needs exactly d = m - r added to it, and
  the move that supplies it must carry a value congruent to d modulo m.
  The usable values are 0, 1, 2, ... in order, so the values congruent to
  d are d, d + m, d + 2m, ...; if c elements need the same d, the last one
  consumes d + (c - 1) * m, and the answer is that largest consumed value
  plus one (x must tick past it). Residue classes never compete for a
  value, so only the worst class matters. A class with a bigger count
  always dominates one with a smaller count — a whole extra multiple of m
  outweighs any difference in d — and among classes tied on count the one
  with the smallest residue r needs the largest d = m - r, which is why
  the scan tracks the max count and breaks ties toward the smallest key.
  Elements already divisible by m are skipped, and an all-divisible array
  needs 0 moves. O(n) time and space.
"""
import sys
from collections import Counter


def solve(n: int, m: int, a_list: list[int]) -> int:
    d = Counter(a % m for a in a_list if a % m != 0)

    mx_val = 0
    mn_key = 2**31-1

    for key, val in d.items():
        if val == mx_val:
            mn_key = min(mn_key, key)
        elif val > mx_val:
            mx_val = val
            mn_key = key

    if not d:
        return 0
    return (mx_val - 1) * m + (m-mn_key) + 1


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
        # Official samples (codeforces.com/problemset/problem/1374/D)
        assert solve(4, 3, [1, 2, 1, 3]) == 6
        assert solve(10, 6, [8, 7, 1, 8, 3, 7, 5, 10, 8, 9]) == 18
        assert solve(5, 10, [20, 100, 50, 20, 100500]) == 0
        assert solve(10, 25, [24] * 10) == 227
        assert solve(8, 8, [1, 2, 3, 4, 5, 6, 7, 8]) == 8
        print("1374d.py: all tests passed")
