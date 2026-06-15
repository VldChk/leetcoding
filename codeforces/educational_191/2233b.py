"""
Codeforces 2233B - Different Distances  (Educational Round 191)
https://codeforces.com/contest/2233/problem/B

For a given n (2 <= n <= 200) construct an array of 4*n integers in which
each value 1, 2, ..., n appears exactly four times and, for every value,
the three gaps between its consecutive occurrences -- (p2 - p1),
(p3 - p2), (p4 - p3) -- are pairwise distinct. Any valid array is
accepted; the problem guarantees one exists.

Input: t test cases, each a single integer n.
Output: 4*n space-separated integers per test case.

Solution idea:
  A fixed deterministic layout works: concatenate [1..n], [1..n],
  [2..n], [1], [1..n]. Every value 2..n then lands with consecutive gaps
  {n-1, n, n+1}, and value 1 with gaps {1, n, 2n-1} -- pairwise distinct
  in both cases for n >= 2. O(n) per test case. (See 2233b_random.py for
  a shuffle-until-valid variant of the same task.)
"""
def solve(n):
    res = []
    res.extend([i for i in range(1, n+1)])
    res.extend([i for i in range(1, n+1)])
    res.extend(range(2, n + 1))
    res.append(1)
    res.extend(range(1, n + 1))

    return " ".join(map(str, res))


if __name__ == '__main__':
    # "Different Distances" is special-judged (any valid array is
    # accepted), so validate the structure rather than match a fixed
    # answer: 4n numbers, each of 1..n exactly four times, and for every
    # value the three consecutive gaps pairwise distinct.
    def _valid(n):
        arr = list(map(int, solve(n).split()))
        if len(arr) != 4 * n:
            return False
        pos = {}
        for i, v in enumerate(arr):
            pos.setdefault(v, []).append(i)
        for v in range(1, n + 1):
            p = pos.get(v, [])
            if len(p) != 4:
                return False
            if len({p[1] - p[0], p[2] - p[1], p[3] - p[2]}) != 3:
                return False
        return True

    for _n in range(2, 61):
        assert _valid(_n), f"invalid arrangement for n={_n}"
    print("2233b.py: all tests passed")


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        print(solve(n))