"""
Codeforces 1539C - Stable Groups  (Round 727, Div. 2)  [rating 1200]
https://codeforces.com/problemset/problem/1539/C

n students have levels a_i. A group is stable if, once its levels are
sorted, no two neighbours differ by more than x. Teachers may invite up
to k extra students of any levels they like. Split everyone into the
fewest stable groups possible.

Note the input line is "n k x" while the function below takes
(n, x, k, a_list) — the caller reorders them.

Sample (n, x, k, a -> groups):
  8,  3,  2, [1, 1, 5, 8, 12, 13, 20, 22]                     -> 2
  13, 37, 0, [20, 20, 80, 70, 70, 70, 420, 5, 1, 5, 1, 60, 90] -> 3

Solution idea:
  Sort the levels. Every adjacent difference greater than x is a break
  that splits the line into one more group, so with no invitations the
  answer is (number of such gaps) + 1. A gap of size g can be stitched
  shut by dropping in enough intermediate students to make each step at
  most x, which needs ceil(g / x) - 1 = (g - 1) // x of them. Each gap
  closed removes exactly one group regardless of its size, so every gap
  is worth the same and only its price differs — sort the prices and buy
  from cheapest upward while the budget k lasts. O(n log n) time.
"""
import sys
from itertools import pairwise


def solve(n: int, x: int, k: int, a_list: list) -> int:
    a_list.sort()
    fisrt_pass = 1
    gaps = []
    for a, b in pairwise(a_list):
        if b - a > x:
            fisrt_pass += 1
            gaps.append(b - a)

    gaps.sort()

    for gap in gaps:
        needed = (gap - 1) // x
        if k >= needed and (k - needed) >= 0:
            k -= needed
            fisrt_pass -= 1
    return fisrt_pass


def main(data: str) -> None:
    it = iter(data.split('\n'))
    n, k, x = map(int, next(it).split())
    a_list = [int(v) for v in next(it).split()]
    sys.stdout.write(str(solve(n, x, k, a_list)) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/problemset/problem/1539/C)
        assert solve(8, 3, 2, [1, 1, 5, 8, 12, 13, 20, 22]) == 2
        assert solve(13, 37, 0,
                     [20, 20, 80, 70, 70, 70, 420, 5, 1, 5, 1, 60, 90]) == 3
        print("1539c.py: all tests passed")
