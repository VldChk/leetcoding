"""
Codeforces 2233B - Different Distances  (Educational Round 191) -- random
https://codeforces.com/contest/2233/problem/B

Alternative solution to 2233b.py (see that file for the full statement).
Instead of a fixed layout, this builds the 4*n array from four blocks,
each a permutation of [1..n], and reshuffles them until the validity
condition holds: for every value the three gaps between its consecutive
occurrences must be pairwise distinct.

Solution idea:
  With blocks of equal width n, a value at within-block offsets
  (a, b, c, d) has real consecutive gaps n+(b-a), n+(c-b), n+(d-c); these
  are pairwise distinct iff the offset deltas (a-b), (b-c), (c-d) are,
  which is exactly what is_valid() checks. Keep random.shuffle-ing the
  four blocks until is_valid() passes (few retries for these limits).
"""
import random
def solve(n):
    def is_valid(part_one, part_two, part_three, part_four):
        pos = [[0 for _ in range(4)] for _ in range(n)]
        for i, p in enumerate(part_one):
            pos[p-1][0] = i
        for i, p in enumerate(part_two):
            pos[p-1][1] = i
            pos[p-1][0] -= i
        for i, p in enumerate(part_three):
            pos[p-1][2] = i
            pos[p-1][1] -= i
        for i, p in enumerate(part_four):
            pos[p-1][3] = i
            pos[p-1][2] -= i
        for i in range(n):
            if pos[i][0] == pos[i][1] or pos[i][1] == pos[i][2] or pos[i][2] == pos[i][0]:
                return False
        return True

    tmp = [i for i in range(1, n+1)]
    part_one = tmp.copy()
    random.shuffle(tmp)
    part_two = tmp.copy()
    random.shuffle(tmp)
    part_three = tmp.copy()
    random.shuffle(tmp)
    part_four = tmp.copy()
    while not is_valid(part_one, part_two, part_three, part_four):
        random.shuffle(part_one)
        random.shuffle(part_two)
        random.shuffle(part_three)
        random.shuffle(part_four)
    
    res = []
    res.extend(part_one)
    res.extend(part_two)
    res.extend(part_three)
    res.extend(part_four)

    # interim = [list(i) for i in zip(part_one, part_two)]
    # part_three = [i for x_i in interim for i in x_i]
    # if n <= 3:
    #     part_five = [n-1, n] + [i for i in range(1, n-1)]
    # else:
    #     part_five = [n-2, n-1, n] + [i for i in range(1, n-2)]
    # part_three.extend(part_one)
    # part_three.extend(part_five)
    # part_one.extend(part_five)
    return ' '.join(str(i) for i in res)


if __name__ == '__main__':
    # Same special-judged task as 2233b.py; validate the structure. The
    # range is kept modest because the solver reshuffles until valid.
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

    for _n in range(2, 26):
        assert _valid(_n), f"invalid arrangement for n={_n}"
    print("2233b_random.py: all tests passed")


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        print(solve(n))