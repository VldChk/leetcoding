"""
Codeforces 2266D - Falling Concrete  (Round 1122, Div. 3)
https://codeforces.com/contest/2266/problem/D

A road has n sections, the i-th of height a_i. One operation picks indices
i < j, lifts section j and carries it back to position i; one unit of
concrete drops onto every section it passes over. Formally the subarray
[a_i, ..., a_j] becomes [a_j - (j - i), a_i + 1, ..., a_{j-1} + 1]. A flat
part is a contiguous run of equal heights. After any number of operations,
find the greatest possible length of a flat part.

Sample (heights -> longest flat part):
  [5 5 5 9 8]                 -> 4     [6 6 6 6 6 6]            -> 6
  [5 6 7 8 9]                 -> 1     [9 7 12 10 12]           -> 5
  [4 7 5 8]                   -> 4     [14 9 14 12 8 11 12]     -> 2
  [1e9 x5]                    -> 5     [8 8 12 8 14 10 15 13]   -> 6

Solution idea:
  Carrying a section one position back costs it exactly one unit of
  height, and every section it steps over gains one while also shifting
  one position forward. Either way a section's height minus its index is
  untouched, so a_i - i is invariant per section. A flat block of length L
  sitting at positions p, p+1, ... p+L-1 all at height h therefore needs
  the L distinct invariants h-p, h-p-1, ..., h-p-L+1: a run of L
  consecutive integers. So the answer is the longest run of consecutive
  values in the set of invariants, found by starting at each value whose
  predecessor is absent and walking upwards. O(n) expected time with a
  hash set, O(n) space.
"""
import sys


def solve(a_list: list[int]) -> int:
    invariants = [(val - idx + 1) for idx, val in enumerate(a_list)]

    vals = set(invariants)

    res = 0
    for inv in vals:
        if inv - 1 not in vals:
            next_inv = inv
            while next_inv in vals:
                next_inv += 1
            res = max(res, next_inv - inv)

    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        next(it)  # n, implied by the length of the following line
        a_list = [int(v) for v in next(it).split()]
        out.append(str(solve(a_list)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2266/problem/D)
        assert solve([5, 5, 5, 9, 8]) == 4
        assert solve([6, 6, 6, 6, 6, 6]) == 6
        assert solve([5, 6, 7, 8, 9]) == 1
        assert solve([9, 7, 12, 10, 12]) == 5
        assert solve([4, 7, 5, 8]) == 4
        assert solve([14, 9, 14, 12, 8, 11, 12]) == 2
        assert solve([1000000000] * 5) == 5
        assert solve([8, 8, 12, 8, 14, 10, 15, 13]) == 6
        print("2266d.py: all tests passed")
