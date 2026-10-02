"""
Codeforces 2267B - Fashionable Array  (Round 1123, Div. 2)  [rating 800]
https://codeforces.com/contest/2267/problem/B

The mode of an array is the value occurring most often; when several
values tie for most occurrences, the mode is the largest of them. Given
an array a of n integers, permute it however you like so that the sum of
the modes of all n prefixes is as large as possible. Any arrangement
achieving the maximum is accepted.

Example: [2, 3, 2] rearranged to [3, 2, 2] gives prefix modes 3, 3, 2,
summing to 8, which is optimal.

Sample (a -> one optimal arrangement):
  [2, 3, 2]             -> [3, 2, 2]
  [4, 4, 2, 1, 3, 1]    -> [4, 4, 3, 2, 1, 1]
  [1, 3, 2, 4, 2]       -> [4, 1, 3, 2, 2]
  [1, 1, 1, 2]          -> [2, 1, 1, 1]
  [1, 2, 3, 4, 5, 6, 7] -> [7, 1, 2, 3, 4, 5, 6]
  [1, 1, 4, 2, 3, 3, 3, 2] -> [4, 3, 2, 1, 3, 3, 1, 2]
  [4, 3, 3, 3, 2, 1, 4, 1] -> [4, 4, 3, 3, 2, 1, 1, 3]

Solution idea:
  Ties go to the larger value, so the biggest value present only has to
  match the others' counts — not beat them — to stay the mode. Walk the
  distinct values from largest to smallest; for the current value emit one
  copy, then one copy of every smaller value still in stock, and repeat
  until the current value is exhausted. That keeps the current value's
  running count greater than or equal to every smaller value's at all
  times, so it owns every prefix mode in its block, and no larger value is
  ever left unused earlier than necessary. O(n * d) time, O(n) space, with
  d the number of distinct values.
"""
import sys
from collections import Counter


def solve(n: int, a_list: list[int]) -> str:
    freq_cnt = Counter(a_list)
    freq_sorted = dict(sorted(freq_cnt.items(), key=lambda x: -x[0]))
    res = []
    keys = list(freq_sorted.keys())
    for i, val in enumerate(keys):
        if val not in freq_sorted:
            continue
        if freq_sorted[val] == 0:
            del freq_sorted[val]
            continue
        while freq_sorted[val] > 0:
            freq_sorted[val] -= 1
            res.append(val)
            j = i + 1
            while j < len(keys):
                if keys[j] not in freq_sorted:
                    j += 1
                    continue
                res.append(keys[j])
                freq_sorted[keys[j]] -= 1
                if freq_sorted[keys[j]] == 0:
                    del freq_sorted[keys[j]]
                j += 1

        if i == len(keys) - 1:
            while freq_sorted[val] > 0:
                res.append(val)
                freq_sorted[val] -= 1
            del freq_sorted[val]
            continue

    return " ".join(map(str, res))


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a_list = [int(v) for v in next(it).split()]
        out.append(solve(n, a_list))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Any arrangement reaching the maximum is accepted, so the samples are
        # checked by score rather than by byte equality: the answer must be a
        # permutation of the input and must tie the judge's reference answer.
        def _prefix_mode_sum(arr: list[int]) -> int:
            total = 0
            for i in range(len(arr)):
                freq = Counter(arr[:i + 1])
                best = max(freq.values())
                total += max(k for k, v in freq.items() if v == best)
            return total

        # Official samples (codeforces.com/contest/2267/problem/B)
        for _a, _judge in [
            ([2, 3, 2], [3, 2, 2]),
            ([4, 4, 2, 1, 3, 1], [4, 4, 3, 2, 1, 1]),
            ([1, 3, 2, 4, 2], [4, 1, 3, 2, 2]),
            ([1, 1, 1, 2], [2, 1, 1, 1]),
            ([1, 2, 3, 4, 5, 6, 7], [7, 1, 2, 3, 4, 5, 6]),
            ([1, 1, 4, 2, 3, 3, 3, 2], [4, 3, 2, 1, 3, 3, 1, 2]),
            ([4, 3, 3, 3, 2, 1, 4, 1], [4, 4, 3, 3, 2, 1, 1, 3]),
        ]:
            _got = [int(v) for v in solve(len(_a), list(_a)).split()]
            assert Counter(_got) == Counter(_a), (_a, _got)
            assert _prefix_mode_sum(_got) == _prefix_mode_sum(_judge), (_a, _got)

        # [2, 3, 2] -> [3, 2, 2] scores 3 + 3 + 2 = 8, as worked in the statement
        assert _prefix_mode_sum([3, 2, 2]) == 8
        print("2267b.py: all tests passed")
