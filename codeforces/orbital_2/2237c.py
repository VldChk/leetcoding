"""
Codeforces 2237C - Duck Surplus  (Order Capital Round 2 / Round 1104, Div. 1 + Div. 2)
https://codeforces.com/contest/2237/problem/C

n piles of rubber ducks stand in a row, the i-th holding a_i ducks. While
a is not sorted in non-decreasing order, Ja must repeat this operation:
pick an index i with a_i > a_{i+1}, then replace the pair (a_i, a_{i+1})
with (a_{i+1}, a_i + a_{i+1}) — the piles swap and the new right pile
absorbs the new left one. So 7 and 3 become 3 and 10. The process always
terminates; Ja picks the indices to make the final largest pile as small
as possible. Report that minimum.

Sample (piles -> smallest possible largest pile):
  [1 2 2 5]             -> 5      [7 3]                    -> 10
  [3 2 1]               -> 6      [2 2 1 3 3]              -> 3
  [3 1 4 2]             -> 6      [1 4 3 2 5]              -> 14
  [6 2 5 1 4 3]         -> 21     [2 7 1 6 3 5 4]          -> 26
  [8 1 7 2 6 3 5 4]     -> 36     [1e9 .. 999999996]       -> 4999999990

Solution idea:
  Ducks are never destroyed, so any pile that sits below its left
  neighbour is forced to absorb it eventually — the order of operations
  cannot avoid that, only shuffle when it happens. Sweep left to right
  keeping the current wall height: while the next pile is at least the
  wall it just becomes the new wall, and when it is below the wall it
  swallows it and becomes their sum (which is necessarily the new, taller
  wall). The answer is the tallest value present after the sweep. O(n)
  time, O(1) extra space.
"""
import sys


def solve(h):
    i = 1
    while i < len(h):
        if h[i] >= h[i-1]:
            i += 1
            continue
        else:
            h[i] += h[i-1]
    return max(h)


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
        # Official samples (codeforces.com/contest/2237/problem/C).
        # solve() rewrites its argument in place, so pass fresh lists.
        assert solve([1, 2, 2, 5]) == 5
        assert solve([7, 3]) == 10
        assert solve([3, 2, 1]) == 6
        assert solve([2, 2, 1, 3, 3]) == 3
        assert solve([3, 1, 4, 2]) == 6
        assert solve([1, 4, 3, 2, 5]) == 14
        assert solve([6, 2, 5, 1, 4, 3]) == 21
        assert solve([2, 7, 1, 6, 3, 5, 4]) == 26
        assert solve([8, 1, 7, 2, 6, 3, 5, 4]) == 36
        assert solve([1000000000, 999999999, 999999998, 999999997, 999999996]) == 4999999990
        print("c.py: all tests passed")
