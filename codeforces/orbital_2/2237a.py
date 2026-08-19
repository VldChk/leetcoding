"""
Codeforces 2237A - Destroying Towers  (Order Capital Round 2 / Round 1104, Div. 1 + Div. 2)
https://codeforces.com/contest/2237/problem/A

n towers stand in a line, the i-th of height a_i. Quack operates on every
tower exactly once, in any order he likes. Operating on tower i shoots a
laser to the right and cuts the first taller tower down to tower i's
height: let j be the smallest index with j > i and a_j > a_i (using the
current heights); if such a j exists, a_j becomes a_i, otherwise nothing
happens. Find the minimum possible final sum of all heights.

Sample (heights -> minimum sum):
  [1, 3, 5]          -> 3     [5, 4, 3]          -> 12
  [3, 2, 5, 1]       -> 8     [2, 1, 4, 3]       -> 5
  [4, 1, 3, 5, 2]    -> 8     [2, 2, 3, 1, 4]    -> 8
  [7]                -> 7     [6, 1, 5, 2, 4, 3] -> 11
  [1, 1, 1, 1]       -> 4     [10, 3, 8, 6, 9]   -> 22

Solution idea:
  A tower is only ever cut by a tower to its left, so tower i can never
  drop below min(a_1..a_i) — that prefix minimum is a lower bound on its
  final height. It is also reachable: operating right to left lets the
  running minimum propagate rightwards one tower at a time, so every
  tower ends at exactly the prefix minimum. The answer is the sum of
  prefix minima. O(n) time, O(1) extra space.
"""
import sys


def solve(h):
    for i in range(1, len(h)):
        h[i] = min(h[i-1], h[i])
    return sum(h)


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        next(it)  # n, implied by the length of the following line
        h = [int(v) for v in next(it).split()]
        out.append(str(solve(h)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2237/problem/A).
        # solve() rewrites its argument in place, so pass fresh lists.
        assert solve([1, 3, 5]) == 3
        assert solve([5, 4, 3]) == 12
        assert solve([3, 2, 5, 1]) == 8
        assert solve([2, 1, 4, 3]) == 5
        assert solve([4, 1, 3, 5, 2]) == 8
        assert solve([2, 2, 3, 1, 4]) == 8
        assert solve([7]) == 7
        assert solve([6, 1, 5, 2, 4, 3]) == 11
        assert solve([1, 1, 1, 1]) == 4
        assert solve([10, 3, 8, 6, 9]) == 22
        print("a.py: all tests passed")
