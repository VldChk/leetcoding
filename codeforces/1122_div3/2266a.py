"""
Codeforces 2266A - Good Contest  (Round 1122, Div. 3)
https://codeforces.com/contest/2266/problem/A

A contest has three problems — easy, medium and hard — and n participants.
A participant is weak if they did not solve all three problems. The
scoreboard is lost; all that remains is an array a of length 3 where a_i
is the number of participants who solved problem i. Over all scoreboards
consistent with a, find the minimum possible number of weak participants.

Sample (n; a -> weak participants):
  3; [3, 3, 3] -> 0      4; [4, 4, 3] -> 1
  1; [1, 1, 1] -> 0      9; [9, 8, 9] -> 1
  5; [0, 5, 5] -> 5      6; [4, 3, 2] -> 4

Solution idea:
  A participant counts as strong only by solving all three problems, so
  the number of strong participants cannot exceed min(a) — the scarcest
  problem caps it. That bound is always reachable: give min(a) people all
  three problems and hand every remaining solve to somebody else, who is
  weak regardless of how many extra problems they pick up. So the answer
  is n - min(a). O(1) time and space.
"""
import sys


def solve(n: int, a_list: list[int]) -> int:
    return n - min(a_list)


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
        # Official samples (codeforces.com/contest/2266/problem/A)
        assert solve(3, [3, 3, 3]) == 0
        assert solve(4, [4, 4, 3]) == 1
        assert solve(1, [1, 1, 1]) == 0
        assert solve(9, [9, 8, 9]) == 1
        assert solve(5, [0, 5, 5]) == 5
        assert solve(6, [4, 3, 2]) == 4
        print("2266a.py: all tests passed")
