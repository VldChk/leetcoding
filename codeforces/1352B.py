"""
Codeforces 1352B - Same Parity Summands  (Round 640, Div. 4)
https://codeforces.com/problemset/problem/1352/B

You are given two positive integers n and k. Represent n as the sum of k
positive integers that all have the same parity — all odd or all even —
or report that no such representation exists. Any valid representation
is accepted.

Sample (n k -> one accepted answer):
  10 3 -> YES 4 2 4             100 4 -> YES 55 5 5 35
  8 7  -> NO                    97 2  -> NO
  8 8  -> YES 1 1 1 1 1 1 1 1   3 10  -> NO
  5 3  -> YES 3 1 1
  1000000000 9 -> YES 111111110 (eight times) 111111120

Solution idea:
  Use k-1 copies of the smallest summand of the chosen parity and put the
  remainder in the last slot. All-odd works when n >= k and n - k is even
  (k-1 ones plus an odd remainder); all-even works when n is even and
  n >= 2k (k-1 twos plus an even remainder). An odd n can never be split
  into an even count, an even n split into an odd count must use evens,
  and every other case uses odds; a non-positive remainder means NO.
  O(k) time and space.
"""
import sys


def solve(x, y):
    is_odd_x = x % 2 != 0
    is_odd_y = y % 2 != 0

    if is_odd_x and not is_odd_y:
        return ("NO", None)

    if not is_odd_x and is_odd_y:
        basis = 2
    else:
        basis = 1

    res = []

    while y > 1:
        res.append(basis)
        x -= basis
        y -= 1

    res.append(x)
    if x <= 0:
        return ("NO", None)
    return ("YES", res)


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, k = (int(v) for v in next(it).split())
        can, res = solve(n, k)
        out.append(can)
        if can == "YES":
            out.append(" ".join(map(str, res)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        def _ok(res, n, k):
            return (len(res) == k and sum(res) == n and min(res) > 0
                    and len({v % 2 for v in res}) == 1)

        # Official samples (codeforces.com/problemset/problem/1352/B). Any valid
        # split is accepted, so check its properties, not the exact numbers.
        assert _ok(solve(10, 3)[1], 10, 3)
        assert _ok(solve(100, 4)[1], 100, 4)
        assert solve(8, 7) == ("NO", None)
        assert solve(97, 2) == ("NO", None)
        assert _ok(solve(8, 8)[1], 8, 8)
        assert solve(3, 10) == ("NO", None)
        assert _ok(solve(5, 3)[1], 5, 3)
        assert _ok(solve(1000000000, 9)[1], 1000000000, 9)
        print("1352B.py: all tests passed")
