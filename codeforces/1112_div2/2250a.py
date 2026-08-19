"""
Codeforces 2250A - Threshold Movement  (Round 1112, Div. 2)
https://codeforces.com/contest/2250/problem/A

There are n+2 positions numbered 0..n+1. Position i holds an element of
weight w_i for every 1 <= i <= n; positions 0 and n+1 start empty. You
pick an integer k, and then every element moves exactly once, all at the
same time:
  * if w_i < k the element at position i moves to position i-1;
  * if w_i > k the element at position i moves to position i+1;
  * if w_i = k the whole movement fails immediately.
k is perfect when the movement does not fail and every position from 1
to n ends up holding exactly one element. Decide whether a perfect k
exists.

Sample (weights -> answer):
  [7]                              -> NO
  [3, 1]                           -> YES
  [2, 1]                           -> NO
  [9, 1, 7, 2]                     -> YES
  [9, 8, 7, 1]                     -> NO
  [1000000000, 1, 9, 2, 8, 3]      -> YES

Solution idea:
  Every position stays occupied only if the elements pair up and swap, so
  exactly half of the weights must sit below k and half above it — the
  threshold has to fall in the gap next to the median of the sorted
  weights. If the two sorted values straddling that gap differ by exactly
  1 there is no integer between them and the answer is NO. Otherwise fix
  the candidate k, then walk the original array and mark each element's
  destination: a weight equal to k, an element at an end that would walk
  off the row, or two elements claiming the same destination all mean NO.
  O(n log n) time, O(n) space.
"""
import sys


def solve(h_orig):
    h = sorted(h_orig)
    if len(h) == 1:
        return "NO"
    elif len(h) % 2 == 0:
        if h[len(h) // 2] - h[len(h) // 2 - 1] == 1:
            return "NO"
    else:
        if h[len(h) // 2] - h[len(h) // 2 - 1] == 1 and h[len(h) // 2 + 1] - h[len(h) // 2] == 1:
            return "NO"

    marked = [False] * (len(h) + 2)

    if len(h) % 2 == 0:
        mid_val = h[len(h) // 2] - 1
    else:
        if h[len(h) // 2] - h[len(h) // 2 - 1] > 1:
            mid_val = h[len(h) // 2] - 1
        else:
            mid_val = h[len(h) // 2] + 1

    if h_orig[0] < mid_val or h_orig[-1] > mid_val:
        return "NO"

    for i in range(len(h)):
        if h_orig[i] < mid_val:
            if not marked[i-1]:
                marked[i-1] = True
            else:
                return "NO"
        elif h_orig[i] > mid_val:
            if not marked[i+1]:
                marked[i+1] = True
            else:
                return "NO"
        else:
            return "NO"
    return "YES"


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        next(it)  # n, implied by the length of the following line
        h = [int(v) for v in next(it).split()]
        out.append(solve(h))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2250/problem/A)
        assert solve([7]) == "NO"
        assert solve([3, 1]) == "YES"
        assert solve([2, 1]) == "NO"
        assert solve([9, 1, 7, 2]) == "YES"
        assert solve([9, 8, 7, 1]) == "NO"
        assert solve([1000000000, 1, 9, 2, 8, 3]) == "YES"
        print("2250a.py: all tests passed")
