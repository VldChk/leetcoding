"""
Codeforces 2257B - Gigantomachy  (Round 1117, Div. 2)
https://codeforces.com/contest/2257/problem/B

Two giants face each other across their own mountain ranges. Bea's
mountains have heights a_1..a_n numbered left to right, Ver's have
b_1..b_m numbered right to left; both ranges are non-increasing
(a_i >= a_{i+1}, b_i >= b_{i+1}). Both giants start on their mountain 1.
On his turn a giant throws one boulder at the mountain his opponent is
standing on, lowering it by 1. Then, if the mountain directly in front of
him (index one greater) is higher than the one he stands on, he jumps
onto it. A giant who stands on height 0 with no mountain in front of him
admits defeat. Bea moves first. Report the number of the winner.

Sample (a / b -> winner):
  [1]       / [1]    -> 1      [1]       / [2]    -> 2
  [4]       / [4 1]  -> 2      [4 3 2 1] / [10 1] -> 2
  [4 3 2 1] / [6 5]  -> 1      [4 3 2 1] / [7 5]  -> 2

Solution idea:
  Neither giant ever chooses anything, so the game is just a race: count
  how many boulders it takes to defeat each side, then see who runs out
  first. Because a range is non-increasing, a giant on mountain i only
  jumps forward once its height drops strictly below a_{i+1}, which costs
  a_i - a_{i+1} + 1 hits; the final mountain instead has to be flattened
  to 0, costing a_i hits. Summing those gives the total hits each giant
  can absorb. Bea throws on odd turns, so he wins exactly when Ver needs
  no more hits than Bea does. O(n + m) time, O(1) extra space.
"""
import sys


def solve(n, m, left, right):
    left.append(0)
    right.append(0)
    steps_left = 0
    for i in range(1, n+1):
        if left[i-1] == 1:
            steps_left += 1
        elif left[i] == 0:
            steps_left += left[i-1]
        else:
            steps_left += (left[i-1] - left[i] + 1)

    steps_right = 0
    for i in range(1, m+1):
        if right[i-1] == 1:
            steps_right += 1
        elif right[i] == 0:
            steps_right += right[i-1]
        else:
            steps_right += (right[i-1] - right[i] + 1)

    if steps_left + 1 > steps_right:
        return 1
    else:
        return 2


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, m = (int(v) for v in next(it).split())
        left = [int(v) for v in next(it).split()]
        right = [int(v) for v in next(it).split()]
        out.append(str(solve(n, m, left, right)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2257/problem/B).
        # solve() appends a sentinel to its arguments, so pass fresh lists.
        assert solve(1, 1, [1], [1]) == 1
        assert solve(1, 1, [1], [2]) == 2
        assert solve(1, 2, [4], [4, 1]) == 2
        assert solve(4, 2, [4, 3, 2, 1], [10, 1]) == 2
        assert solve(4, 2, [4, 3, 2, 1], [6, 5]) == 1
        assert solve(4, 2, [4, 3, 2, 1], [7, 5]) == 2
        print("2257B.py: all tests passed")
