"""
Codeforces 1283C - Friends and Gifts  (Round 611, Div. 3)
https://codeforces.com/problemset/problem/1283/C

n friends each give exactly one gift and receive exactly one gift, and
nobody may give to themselves. For each friend f_i is known: 0 if they have
not decided, otherwise the friend they will give to. All non-zero f_i are
distinct, at least two are zero, and the input is never contradictory.
Fill in the zeros so the result is a permutation with no fixed point. Any
valid answer is accepted.

Sample (f -> one accepted answer):
  [5 0 0 2 4]        -> 5 3 1 2 4
  [7 0 0 1 4 0 6]    -> 7 3 2 1 4 5 6
  [7 4 0 3 0 5 1]    -> 7 4 2 3 6 5 1
  [2 1 0 0 0]        -> 2 1 4 5 3

Solution idea:
  The friends with f_i = 0 are exactly the givers still unassigned, and the
  numbers missing from f are exactly the receivers nobody gives to yet, so
  the two sets have equal size and any pairing between them works apart
  from the self-gift rule. Walk the undecided givers and hand each the next
  free receiver, stepping over the one that would be their own index. The
  only awkward case is the very last giver being left with themselves; then
  swap that receiver with the one handed out on the previous step, which is
  always legal because that other giver has a different index.
  O(n log n) time for the sort, O(n) space.
"""
import sys


def solve(a_list: list[int]) -> str:
    s_list = [i+1 for i in range(len(a_list))]
    s_a_list = sorted(a_list)
    s_a_list = [i for i in s_a_list if i != 0]
    empty_indices = []
    j = 0
    for i, a in enumerate(s_list):
        if j < len(s_a_list) and a == s_a_list[j]:
            j += 1
        else:
            empty_indices.append(a)
    prev_assignment: tuple[int, ...] = ()
    for i, a in enumerate(a_list):
        if a == 0:
            if empty_indices[-1] == i+1:
                if len(empty_indices) < 2:
                    # repairing from the previous assignment
                    a_list[i] = prev_assignment[0]
                    a_list[prev_assignment[1]] = empty_indices[-1]
                else:
                    a_list[i] = empty_indices[-2]
                    prev_assignment = (empty_indices.pop(-2), i)
            else:
                a_list[i] = empty_indices[-1]
                prev_assignment = (empty_indices.pop(), i)

    return " ".join(map(str, a_list))


def main(data: str) -> None:
    it = iter(data.split('\n'))
    next(it)  # n, implied by the length of the following line
    a_list = [int(v) for v in next(it).split()]
    sys.stdout.write(solve(a_list) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        def _ok(res: str, f: list[int]) -> bool:
            vals = [int(x) for x in res.split()]
            if sorted(vals) != list(range(1, len(f) + 1)):
                return False
            return all(v != i and (orig == 0 or v == orig)
                       for i, (v, orig) in enumerate(zip(vals, f), start=1))

        # Official samples (codeforces.com/problemset/problem/1283/C). Any valid
        # assignment is accepted, so check the properties, not the exact numbers.
        # solve() fills its list argument in place, so pass a fresh list.
        assert _ok(solve([5, 0, 0, 2, 4]), [5, 0, 0, 2, 4])
        assert _ok(solve([7, 0, 0, 1, 4, 0, 6]), [7, 0, 0, 1, 4, 0, 6])
        assert _ok(solve([7, 4, 0, 3, 0, 5, 1]), [7, 4, 0, 3, 0, 5, 1])
        assert _ok(solve([2, 1, 0, 0, 0]), [2, 1, 0, 0, 0])
        print("1283c.py: all tests passed")
