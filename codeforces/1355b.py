"""
Codeforces 1355B - Young Explorers  (Round 642, Div. 1 B / Div. 2 D)  [rating 1200]
https://codeforces.com/problemset/problem/1355/B

Each young explorer has an inexperience e_i, and an explorer with
inexperience e may only join a group of e or more people. Not everyone
has to be placed — some may stay in the camp. Form as many groups as
possible.

Sample (a -> groups):
  [1, 1, 1]       -> 3
  [2, 3, 1, 2, 2] -> 2

Solution idea:
  Sort the inexperiences ascending and sweep, keeping a running count of
  explorers held back for the group being assembled. Because the array is
  sorted, the explorer currently being added always has the largest
  requirement in that pending bunch, so the moment the count reaches his
  e every member of the bunch is satisfied — close the group and reset
  the counter. Closing a group as soon as it becomes legal is optimal:
  carrying extra members forward can only delay the next group, never
  enable one, since every later requirement is at least as large.
  O(n log n) time for the sort, O(1) extra space.
"""
import sys


def solve(n: int, a_list: list) -> int:
    a_list.sort()
    res = 0
    curr = 0
    for a in a_list:
        curr += 1
        if curr >= a:
            res += 1
            curr = 0
    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a_list = [int(v) for v in next(it).split()]
        out.append(str(solve(n, a_list)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/problemset/problem/1355/B)
        assert solve(3, [1, 1, 1]) == 3
        assert solve(5, [2, 3, 1, 2, 2]) == 2
        print("1355b.py: all tests passed")
