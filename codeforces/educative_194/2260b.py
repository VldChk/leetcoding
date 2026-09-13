"""
Codeforces 2260B - Monocarp and Projects  (Educational Round 194)
https://codeforces.com/contest/2260/problem/B

Over k months Monocarp's company has x + i employees and y + i projects in
month i (0 <= i < k). With a employees and b projects in a month, every
employee gets floor(b / a) projects and Monocarp completes the remaining
b mod a himself. Find the total number of projects Monocarp completes over
all k months.

Sample (x y k -> total):
  1 1 1     -> 0          3 10 2   -> 4          3 8 6 -> 18
  7 20 1    -> 6          10 25 100 -> 1425      8 36 17 -> 110
  1 999900 1000000000000 -> 999898177699820694

Solution idea:
  Let d = y - x. Month i asks for (x + i + d) mod (x + i), which is
  d mod (x + i): the gap between projects and employees never changes.
  From month i = d onwards x + i > d, so the remainder is exactly d. Sum
  d mod (x + i) directly for the first min(d, k) months, then add d for
  each of the remaining k - d months. k can reach 10^12, but the loop runs
  fewer than d < 10^6 times, bounded by the sum of y. O(min(y - x, k)) per
  test case, O(1) space.
"""
import sys


def solve(x, y, k):
    res = 0
    div = 0
    for i in range(min(y-x, k)):
        div = (y-x) % (x+i)
        res += div
    if y-x < k:
        res += ((y-x)) * (k - (y-x))
    return res


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        x, y, k = (int(v) for v in next(it).split())
        out.append(str(solve(x, y, k)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2260/problem/B)
        assert solve(1, 1, 1) == 0
        assert solve(3, 10, 2) == 4
        assert solve(3, 8, 6) == 18
        assert solve(7, 20, 1) == 6
        assert solve(10, 25, 100) == 1425
        assert solve(8, 36, 17) == 110
        assert solve(1, 999900, 1000000000000) == 999898177699820694
        print("2260b.py: all tests passed")
