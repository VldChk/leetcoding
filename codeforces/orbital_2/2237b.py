"""
Codeforces 2237B - Annoying the Ghost  (Order Capital Round 2 / Round 1104, Div. 1 + Div. 2)
https://codeforces.com/contest/2237/problem/B

Ja has n piles of rubber ducks in a row, the i-th holding a_i ducks, and
is told to turn them into the strictly increasing sequence b_1 < ... < b_n
using two stages, in this order:
  * stage 1 — add any non-negative number of ducks to each pile;
  * stage 2 — repeatedly swap two adjacent piles.
Find the minimum number of stage-2 swaps over all valid processes, or -1
if no process works.

Sample (a / b -> swaps):
  [1 2 2]         / [1 3 5]       -> 0     [2 2 1]         / [1 2 3]       -> 2
  [5 1]           / [2 4]         -> -1    [6 5 4 3 2 1]   / [1..6]        -> 15
  [4 7 1 6 2 5 3] / [1..7]        -> 12    [2 1]           / [2 3]         -> 0
  [3 2 2 1]       / [1 2 3 4]     -> 4     [4 3 2 1]       / [1 3 4 5]     -> 4
  [1 5 4 3 2]     / [2 3 4 5 6]   -> 3     [10 3 8 6 9]    / [3 6 8 9 10]  -> 5

Solution idea:
  Ducks can only be added, so a pile holding a_i must end up at some
  target b_j >= a_i, and since b is strictly increasing each target is
  used exactly once. Scanning the piles left to right and greedily
  claiming the smallest still-unused target that is >= a_i is optimal —
  taking a larger one can only starve a later pile. If any pile finds no
  target left the answer is -1. That assignment fixes a permutation p of
  target positions, and the fewest adjacent swaps that sort a permutation
  is exactly its inversion count, which a merge sort counts while
  sorting. O(n^2) here because "first unused index" is a list scan and
  pop; a Fenwick tree would make it O(n log n). n <= 2000, so this is fine.
"""
import sys
from bisect import bisect_left


def solve(n, a, b):
    if max(a) > max(b):
        return -1

    def merge(left, mid, right):
        swap_count = 0
        i = left
        j = mid
        k = left
        while (i <= mid - 1) and (j <= right):
            temp[k] = a[i] if a[i] <= a[j] else a[j]
            k += 1
            if a[i] <= a[j]:
                i += 1
            else:
                j += 1
                swap_count += mid - i
        while i <= mid - 1:
            temp[k] = a[i]
            k += 1
            i += 1

        while j <= right:
            temp[k] = a[j]
            k += 1
            j += 1

        for i in range(left, right + 1):
            a[i] = temp[i]
        return swap_count

    def merge_sort(left, right):
        swap_count = 0
        if left < right:
            mid = (left + right) // 2
            swap_count += merge_sort(left, mid)
            swap_count += merge_sort(mid + 1, right)
            swap_count += merge(left, mid + 1, right)
        return swap_count

    temp = [0] * n

    available = list(range(n))  # unused b indices: [0, 1, 2, ..., n - 1]
    p = []

    for x in a:
        lo = bisect_left(b, x)  # first b[j] where b[j] >= x
        pos = bisect_left(available, lo)  # first unused index >= lo

        if pos == len(available):
            return -1

        j = available.pop(pos)  # claim b[j]
        p.append(j)

    a = p.copy()

    swap_count = merge_sort(0, n - 1)

    for i in range(n):
        if a[i] > b[i]:
            return -1

    return swap_count


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(v) for v in next(it).split()]
        b = [int(v) for v in next(it).split()]
        out.append(str(solve(n, a, b)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2237/problem/B)
        assert solve(3, [1, 2, 2], [1, 3, 5]) == 0
        assert solve(3, [2, 2, 1], [1, 2, 3]) == 2
        assert solve(2, [5, 1], [2, 4]) == -1
        assert solve(6, [6, 5, 4, 3, 2, 1], [1, 2, 3, 4, 5, 6]) == 15
        assert solve(7, [4, 7, 1, 6, 2, 5, 3], [1, 2, 3, 4, 5, 6, 7]) == 12
        assert solve(2, [2, 1], [2, 3]) == 0
        assert solve(4, [3, 2, 2, 1], [1, 2, 3, 4]) == 4
        assert solve(4, [4, 3, 2, 1], [1, 3, 4, 5]) == 4
        assert solve(5, [1, 5, 4, 3, 2], [2, 3, 4, 5, 6]) == 3
        assert solve(5, [10, 3, 8, 6, 9], [3, 6, 8, 9, 10]) == 5
        print("b.py: all tests passed")
