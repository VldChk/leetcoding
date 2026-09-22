# Solved outside of the contest; no rating is acquired
from functools import cache

PRIMES: list[int] = []
divisors: list[list[int]] = [[] for _ in range(2 * 10 ** 5 + 1)]

def get_primes_up_to_a(k: int) -> None:
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


def get_first_prime_divisor(i: int) -> int:
    global PRIMES
    for p in reversed(PRIMES):
        if p > i:
            continue
        if i % p == 0:
            return p
    return 1


def unwrap_a_below_k(dp:list[int], a: int, k: int) -> int:
    global divisors
    if dp[a] != -1:
        return dp[a]
    # print(f"unwrap_a_below_k called with a={a}, k={k}")
    if a <= k:
        dp[a] = 0
        return 0
    r = min(1 + d * unwrap_a_below_k(dp, a // d, k) for d in divisors[a])
    dp[a] = r
    return r


def solve(a_list: list[int], k: int) -> int:
    max_a = max(a_list)
    dp: list[int] = [-1] * (max_a + 1)
    # a_primes = [p for p in PRIMES if p <= max_a]

    a_list = [a for a in a_list if a > k]
    res = 0
    for a in a_list:
        res += unwrap_a_below_k(dp, a, k)
    return res


if __name__ == '__main__':
    get_primes_up_to_a(2 * 10 ** 5)
    # print(divisors[:20])  # Optional: print the first 20 divisors for verification
    t = int(input().strip())
    for _ in range(t):
        n, k =  [int(x) for x in input().strip().split(' ')]
        a_list: list[int] = [int(x) for x in input().strip().split(' ')]
        print(solve(a_list, k))