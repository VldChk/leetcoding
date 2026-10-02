"""
Codeforces 2266E - Prime Destruction  (Round 1122, Div. 3)
https://codeforces.com/contest/2266/problem/E

You are given a multiset a of n positive integers. One operation picks an
integer x > 1 from the multiset and a prime divisor p of x, removes one
copy of x, and adds p copies of x / p. Given k, let f(k) be the minimum
number of operations needed until every element is at most k. Report f(k).

Solved outside of the contest; no rating was acquired.

Sample (k; multiset -> operations):
  1;  [1]                                  -> 0
  2;  [6 6 4 3 2 1]                        -> 4
  1;  [8 6 4 3 2 1 8 6]                    -> 25
  3;  [12 10 9 8 7 6 5 4 3 2 1 12]         -> 15
  9;  [10 9 8 7 6 5 4 3 2 1]               -> 1
  5;  [5 4 3 2 1]                          -> 0

Solution idea:
  Splitting one element never touches the others, so the total is just the
  sum of a per-element cost. For a single x, cost(x) = 0 when x <= k;
  otherwise one operation turns x into p copies of x / p, each of which
  must be shrunk in turn, giving
  cost(x) = min over primes p dividing x of 1 + p * cost(x / p).
  The multiplier p is why the cheapest prime is not always the best one,
  so every prime divisor has to be tried. A sieve lists the prime divisors
  of every value up to 2 * 10^5 once, and cost is memoised in a dp array
  per test case. O(A log log A) to sieve plus memoised recursion, where A
  is the value bound.
"""
import sys

PRIMES: list[int] = []
divisors: list[list[int]] = [[] for _ in range(2 * 10 ** 5 + 1)]


def get_primes_up_to_a(k: int) -> None:
    """Fill PRIMES with every prime <= k and divisors[v] with v's prime divisors."""
    global PRIMES
    global divisors
    sieve = [True] * (k + 1)
    sieve[0] = sieve[1] = False
    divisors[0] = divisors[1] = [1]
    for i in range(2, int(k**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, k + 1, i):
                sieve[j] = False
    PRIMES = [i for i, is_prime in enumerate(sieve) if is_prime]
    for p in PRIMES:
        for j in range(p, k + 1, p):
            divisors[j].append(p)
    return


def unwrap_a_below_k(dp: list[int], a: int, k: int) -> int:
    global divisors
    if dp[a] != -1:
        return dp[a]
    if a <= k:
        dp[a] = 0
        return 0
    r = min(1 + d * unwrap_a_below_k(dp, a // d, k) for d in divisors[a])
    dp[a] = r
    return r


def solve(a_list: list[int], k: int) -> int:
    max_a = max(a_list)
    dp: list[int] = [-1] * (max_a + 1)

    a_list = [a for a in a_list if a > k]
    res = 0
    for a in a_list:
        res += unwrap_a_below_k(dp, a, k)
    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, k = (int(v) for v in next(it).split())
        a_list = [int(v) for v in next(it).split()]
        out.append(str(solve(a_list, k)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    get_primes_up_to_a(2 * 10 ** 5)
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2266/problem/E)
        assert solve([1], 1) == 0
        assert solve([6, 6, 4, 3, 2, 1], 2) == 4
        assert solve([8, 6, 4, 3, 2, 1, 8, 6], 1) == 25
        assert solve([12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 12], 3) == 15
        assert solve([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 9) == 1
        assert solve([5, 4, 3, 2, 1], 5) == 0
        print("2266e.py: all tests passed")
