"""
Codeforces 2260A - Monocarp's Contest  (Educational Round 194)
https://codeforces.com/contest/2260/problem/A

A contest has n problems in a row, each easy (0) or hard (1). Monocarp
wants the first and the last problems to be easy, and in one operation he
may swap any two problems. Find the minimum number of swaps, or -1 if it
is impossible.

Sample (problems -> swaps):
  [0 0]         -> 0      [0 1]       -> -1
  [1 0 0 1 0 0] -> 1      [1 0 0 1 1] -> 2

Solution idea:
  Both ends can only be easy if there are at least two easy problems in
  total; otherwise the answer is -1. When there are, each hard endpoint is
  fixed by one swap with an easy problem from elsewhere, and a single swap
  never fixes both ends, so the answer is just the number of hard
  endpoints. O(n) time and space.
"""
import sys


def solve(h):
    if h[0] == 0 and h[-1] == 0:
        return 0
    elif len([x for x in h if x == 0]) < 2:
        return -1
    else:
        return (h[0] == 1) + (h[-1] == 1)


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        next(it)  # n, implied by the length of the following line
        h = [int(v) for v in next(it).split()]
        out.append(str(solve(h)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2260/problem/A)
        assert solve([0, 0]) == 0
        assert solve([0, 1]) == -1
        assert solve([1, 0, 0, 1, 0, 0]) == 1
        assert solve([1, 0, 0, 1, 1]) == 2
        print("2260a.py: all tests passed")
