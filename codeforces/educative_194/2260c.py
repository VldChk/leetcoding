"""
Codeforces 2260C - Maximize XOR, Minimize Operations  (Educational Round 194)
https://codeforces.com/contest/2260/problem/C

You are given non-negative integers x and y. One operation decreases x by
1 and increases y by 1, and is not allowed when x = 0. Perform some number
of operations so that x XOR y becomes as large as possible and, among all
ways to reach that maximum, use the fewest operations. Output the maximum
XOR and that minimum number of operations.

Sample (x y -> max XOR, operations):
  3 1 -> 4 3
  0 5 -> 5 0
  6 4 -> 10 4

Solution idea:
  Operations keep s = x + y fixed, and x XOR y <= x + y with equality
  exactly when the two numbers share no set bit. Splitting the bits of s
  between them reaches that bound (x' = 0 always qualifies), so the
  maximum XOR is s itself. Operations only lower x, so the cost is x - x'
  for a submask x' of s with x' <= x; minimise it by making x' as large as
  possible: walk the bits of s from high to low and keep each one while
  the running value stays <= x. A higher bit outweighs all lower bits
  combined, so this greedy is optimal. O(log s) time, O(1) space.
"""
import sys


def solve(x, y):
    max_xor = 0 ^ (x + y)
    a = 0

    for bit in range(max_xor.bit_length() - 1, -1, -1):
        value = 1 << bit

        if max_xor & value:
            if a + value <= x:
                a |= value

    return f"{max_xor} {x-a}"


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        x, y = (int(v) for v in next(it).split())
        out.append(solve(x, y))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == "__main__":
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2260/problem/C)
        assert solve(3, 1) == "4 3"
        assert solve(0, 5) == "5 0"
        assert solve(6, 4) == "10 4"
        print("2260c.py: all tests passed")
