"""
Codeforces 2266B - Three Piles  (Round 1122, Div. 3)
https://codeforces.com/contest/2266/problem/B

Alice starts with a stones, Bob with b stones, and a third pile holds c
stones. They alternate turns with Alice first, and on a turn the current
player may move any number of stones (possibly zero) from the third pile
into their own pile. The game ends once both players take zero on two
consecutive turns. With A and B the final pile sizes, the score is
|A - B|: Alice maximises it, Bob minimises it. Report the score under
optimal play.

Sample (a b c -> score):
  3 6 3   -> 3        3 6 10 -> 7
  5 5 4   -> 4        2 5 6  -> 3
  67676767 41414141 998244353 -> 1024506979

Solution idea:
  Alice has only two strategies worth considering. She can empty the pile
  at once, ending the game at a + c - b. Or she can take nothing, and
  then whatever Bob does he cannot pull the gap below |a - b| — taking
  stones to catch up merely overshoots. Bob, moving second, can never
  improve on closing the difference, so the score is
  max(a + c - b, |a - b|); the first term also covers Alice taking only
  part of the pile. Checked exhaustively against a brute-force game
  search for a, b < 7 and c < 9. O(1) time and space.
"""
import sys


def solve(a_list: list[int]) -> int:
    return max(a_list[0] + a_list[2] - a_list[1], abs(a_list[0] - a_list[1]))


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        a_list = [int(v) for v in next(it).split()]
        out.append(str(solve(a_list)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2266/problem/B)
        assert solve([3, 6, 3]) == 3
        assert solve([3, 6, 10]) == 7
        assert solve([5, 5, 4]) == 4
        assert solve([2, 5, 6]) == 3
        assert solve([67676767, 41414141, 998244353]) == 1024506979
        print("2266b.py: all tests passed")
