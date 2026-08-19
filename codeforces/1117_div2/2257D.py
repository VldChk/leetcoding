"""
Codeforces 2257D - Bermuda Rectangle  (Round 1117, Div. 2)
https://codeforces.com/contest/2257/problem/D

The Bermuda Rectangle has integer sides, area exactly S, and its bottom
left corner at (0, 0) — but which pair of sides it uses is unknown. For a
query (x, y), consider the rectangle with corners (0, 0) and (x, y) and
count how many of its unit cells could lie inside the Bermuda Rectangle,
i.e. how many are covered by at least one rectangle [0, a] x [0, S/a]
with a dividing S. Answer q such queries.

Sample (S; query -> answer):
  S=6; (2,3) -> 6    (4,5) -> 11   (6,6) -> 14   (1,1) -> 1
  S=5; (2,2) -> 3    (3,4) -> 6
  S=8; (3,1) -> 3    (5,6) -> 15

Solution idea:
  The union of all candidate rectangles is a staircase: sort the divisor
  pairs (a, S/a) by increasing width a, so the heights decrease. Build a
  prefix array where pref[i] is the union area of the first i+1
  rectangles, each step adding the strip (xs[i] - xs[i-1]) * ys[i]. A
  query (x, y) then splits in two: every divisor with xs[j] <= S // y is
  tall enough to cover the full height y, so that part contributes a
  clean rectangle, and the rest is a slice of the staircase read off the
  prefix array. Two binary searches locate the boundaries. Building costs
  O(sqrt(S) log S), each query O(log S).
"""
import math
import sys
from bisect import bisect_left, bisect_right


def solve(S, q, queries):
    def find_divisors(n):
        divisors = []
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                divisors.append((i, n // i))
                divisors.append((n // i, i))
        return divisors

    divisors = find_divisors(S)
    divisors.sort()

    xs = [a for a, _ in divisors]
    pref = [S]
    prev_x = 1
    for i in range(1, len(divisors)):
        a, b = divisors[i]
        pref.append(pref[-1] + (a - prev_x) * b)
        prev_x = a

    res = []
    for x, y in queries:
        j = bisect_right(xs, S // y) - 1
        k = bisect_left(xs, x)
        if k <= j:
            r = x * y
        else:
            r = (
                xs[j] * y
                + pref[k - 1] - pref[j]
                + (x - xs[k - 1]) * (S // xs[k])
            )
        res.append(str(r))

    return res


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        S, q = (int(v) for v in next(it).split())
        queries = [tuple(int(v) for v in next(it).split()) for _ in range(q)]
        out.extend(solve(S, q, queries))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2257/problem/D)
        assert solve(6, 4, [(2, 3), (4, 5), (6, 6), (1, 1)]) == ["6", "11", "14", "1"]
        assert solve(5, 2, [(2, 2), (3, 4)]) == ["3", "6"]
        assert solve(8, 2, [(3, 1), (5, 6)]) == ["3", "15"]
        print("2257D.py: all tests passed")
