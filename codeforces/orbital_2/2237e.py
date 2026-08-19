"""
Codeforces 2237E - Permutation Commutation  (Order Capital Round 2 / Round 1104, Div. 1 + Div. 2)
https://codeforces.com/contest/2237/problem/E

You are given a permutation a of length n and an incomplete sequence b of
the same length, where every b_i is either -1 or an integer in 1..n, and
each integer appears at most once in b. Replace every -1 so that b becomes
a permutation commuting with a, i.e. a_{b_i} = b_{a_i} for every
1 <= i <= n. Among all valid completions output the lexicographically
smallest one, or report that none exists.

Sample (a / b -> answer):
  [2 3 1]         / [-1 -1 -1]        -> YES [1 2 3]
  [2 1 4 3]       / [-1 -1 4 -1]      -> YES [1 2 4 3]
  [2 1 4 3]       / [3 1 -1 -1]       -> NO
  [2 1 4 3]       / [1 -1 -1 2]       -> NO
  [2 3 1 5 4]     / [2 -1 -1 -1 -1]   -> YES [2 3 1 4 5]
  [2 3 1 5 4]     / [4 -1 -1 -1 -1]   -> NO
  [2 3 1 5 6 4]   / [4 -1 -1 -1 -1 -1]-> YES [4 5 6 1 2 3]
  [2 1 4 3 6 5]   / [-1 3 -1 -1 -1 -1]-> YES [4 3 1 2 5 6]
  [3 5 6 2 1 4]   / [-1 -1 -1 3 6 -1] -> NO
  [2 3 1 5 4 6 7] / [-1 -1 -1 -1 -1 7 -1]         -> YES [1 2 3 4 5 7 6]
  [2 3 4 1 6 7 8 5] / [5 7 -1 -1 -1 -1 -1 -1]     -> NO
  [2 3 4 1 6 7 8 5] / [5 -1 -1 -1 -1 -1 -1 -1]    -> YES [5 6 7 8 1 2 3 4]

Solution idea:
  Commuting with a means b permutes a's cycles: it maps each cycle onto a
  cycle of the same length, and inside a cycle it acts as a rotation by a
  single fixed shift. So decompose a into cycles and record, for every
  index, its cycle id and its position within that cycle. Each already
  known b_i pins its cycle's target cycle and the shift; a length
  mismatch, two different pins on one cycle, or two cycles claiming the
  same target all mean NO. The still-free cycles are then filled greedily:
  cycles are discovered in increasing order of their smallest index, so
  walking them in that order and handing each the available same-length
  target with the smallest minimum index — aligning the shift so those
  minima line up — yields the lexicographically smallest completion.
  O(n log n) time, O(n) space.
"""
import sys


def solve(t, a, b):

    visited = [False] * (t + 1)

    a = [0] + a
    b = [0] + b

    visited[0] = True
    cycles = []
    cycle_idx = [0] * (t + 1)
    cycle_pos = [0] * (t + 1)

    for i in range(1, t + 1):
        if visited[i]:
            continue

        current_cycle_idx = []

        j = i
        while not visited[j]:
            current_cycle_idx.append(j)
            visited[j] = True
            j = a[j]

        for idx in range(len(current_cycle_idx)):
            cycle_idx[current_cycle_idx[idx]] = len(cycles)
            cycle_pos[current_cycle_idx[idx]] = idx
        cycles.append(current_cycle_idx)

    target = [-1] * len(cycles)
    shift = [0] * len(cycles)

    for i in range(1, t + 1):
        if b[i] == -1:
            continue

        c1 = cycle_idx[i]
        c2 = cycle_idx[b[i]]
        if len(cycles[c1]) != len(cycles[c2]):
            return "NO"

        diff = (cycle_pos[b[i]] - cycle_pos[i]) % len(cycles[c1])
        if target[c1] != -1 and (target[c1] != c2 or shift[c1] != diff):
            return "NO"
        target[c1] = c2
        shift[c1] = diff

    used = [False] * len(cycles)
    for c in target:
        if c == -1:
            continue
        if used[c]:
            return "NO"
        used[c] = True

    available = {}
    for c in range(len(cycles)):
        if used[c]:
            continue
        cycle_len = len(cycles[c])
        if cycle_len not in available:
            available[cycle_len] = []
        available[cycle_len].append((min(cycles[c]), c))

    for cycle_len in available:
        available[cycle_len].sort(reverse=True)

    for c in range(len(cycles)):
        if target[c] != -1:
            continue
        cycle_len = len(cycles[c])
        if cycle_len not in available or not available[cycle_len]:
            return "NO"
        _, target[c] = available[cycle_len].pop()
        shift[c] = cycle_pos[min(cycles[target[c]])]

    for c in range(len(cycles)):
        for idx in range(len(cycles[c])):
            b[cycles[c][idx]] = cycles[target[c]][(idx + shift[c]) % len(cycles[c])]

    return ("YES", b[1:])


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        a = [int(v) for v in next(it).split()]
        b = [int(v) for v in next(it).split()]
        result = solve(n, a, b)
        if result == "NO":
            out.append("NO")
        else:
            out.append("YES")
            out.append(" ".join(map(str, result[1])))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2237/problem/E)
        assert solve(3, [2, 3, 1], [-1, -1, -1]) == ("YES", [1, 2, 3])
        assert solve(4, [2, 1, 4, 3], [-1, -1, 4, -1]) == ("YES", [1, 2, 4, 3])
        assert solve(4, [2, 1, 4, 3], [3, 1, -1, -1]) == "NO"
        assert solve(4, [2, 1, 4, 3], [1, -1, -1, 2]) == "NO"
        assert solve(5, [2, 3, 1, 5, 4], [2, -1, -1, -1, -1]) == ("YES", [2, 3, 1, 4, 5])
        assert solve(5, [2, 3, 1, 5, 4], [4, -1, -1, -1, -1]) == "NO"
        assert solve(6, [2, 3, 1, 5, 6, 4], [4, -1, -1, -1, -1, -1]) == ("YES", [4, 5, 6, 1, 2, 3])
        assert solve(6, [2, 1, 4, 3, 6, 5], [-1, 3, -1, -1, -1, -1]) == ("YES", [4, 3, 1, 2, 5, 6])
        assert solve(6, [3, 5, 6, 2, 1, 4], [-1, -1, -1, 3, 6, -1]) == "NO"
        assert solve(7, [2, 3, 1, 5, 4, 6, 7], [-1, -1, -1, -1, -1, 7, -1]) == ("YES", [1, 2, 3, 4, 5, 7, 6])
        assert solve(8, [2, 3, 4, 1, 6, 7, 8, 5], [5, 7, -1, -1, -1, -1, -1, -1]) == "NO"
        assert solve(8, [2, 3, 4, 1, 6, 7, 8, 5], [5, -1, -1, -1, -1, -1, -1, -1]) == ("YES", [5, 6, 7, 8, 1, 2, 3, 4])
        print("e.py: all tests passed")
