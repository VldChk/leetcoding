"""
Codeforces 2267C - GCD Treasury  (Round 1123, Div. 2)  [rating 1200]
https://codeforces.com/contest/2267/problem/C

There are n piles of coins, pile i holding a_i coins, and the pirate
carries a number x. Repeatedly: he picks an index i with a_i > 0 and
gcd(a_i, x) != 1, lets g = gcd(a_i, x), steals exactly g coins from that
pile (a_i -= g), and then replaces x with g. When no such index exists he
stops. Maximise the total number of coins stolen.

Sample (n, x, a -> coins stolen):
  3, 1, [2, 3, 5]             -> 0
  3, 4, [2, 3, 4]             -> 6
  4, 2, [2, 2, 2, 2]          -> 8
  6, 6, [2, 3, 2, 3, 2, 3]    -> 9
  7, 6, [9, 9, 4, 4, 4, 4, 4] -> 20

Solution idea:
  x is only ever replaced by a divisor of itself, so its set of prime
  factors can only shrink — pick the prime p that survives and the whole
  run is decided. Any pile divisible by p can be emptied completely:
  every steal subtracts gcd(a_i, x), which divides a_i, so the pile stays
  a multiple of p and marches down to exactly 0 while x stays a multiple
  of p. Piles not divisible by p are unreachable once p is the only prime
  left. So committing to p yields exactly the sum of the a_i divisible by
  p, and there is no way to profit from two different primes because x
  can never regain a factor it dropped. The answer is therefore the best
  such sum over the primes dividing x, and 0 when x == 1. Factorising x
  costs O(sqrt x) and each of its at most ~6 distinct primes costs one
  O(n) sweep.
"""
import sys
from typing import Generator


def solve(n: int, x: int, a_list: list[int]) -> int:
    def _find_prime_before_x(x: int) -> Generator[int, None, None]:
        t = x
        if x <= 2:
            yield x
            return
        for num in range(2, int(x**0.5) + 2):
            if t % num == 0:
                yield num
                while t % num == 0:
                    t //= num
                if t == 1:
                    return
            else:
                continue
        yield t
        return

    if x == 1:
        return 0

    res = 0

    for prime in _find_prime_before_x(x):
        t = sum(a for a in a_list if a % prime == 0)
        res = max(res, t)

    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, x = map(int, next(it).split())
        a_list = [int(v) for v in next(it).split()]
        out.append(str(solve(n, x, a_list)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2267/problem/C)
        assert solve(3, 1, [2, 3, 5]) == 0
        assert solve(3, 4, [2, 3, 4]) == 6
        assert solve(4, 2, [2, 2, 2, 2]) == 8
        assert solve(6, 6, [2, 3, 2, 3, 2, 3]) == 9
        assert solve(7, 6, [9, 9, 4, 4, 4, 4, 4]) == 20
        print("2267c.py: all tests passed")
