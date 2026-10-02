"""
Codeforces 2266C - AND, OR, Sort!  (Round 1122, Div. 3)
https://codeforces.com/contest/2266/problem/C

You are given a binary string s of length n. Any number of times you may
pick an index i and replace s_i with either the bitwise AND or the
bitwise OR of the prefix s_1, s_2, ..., s_i (for i = 1 both equal s_1
itself). Find the minimum number of operations needed to make s sorted in
non-decreasing order.

Sample (s -> operations):
  0011     -> 0      1000    -> 3
  01000    -> 1      01001101 -> 2
  0101010  -> 3      0111101  -> 1

Solution idea:
  s_1 can never change, because both the AND and the OR of a one-element
  prefix are that element. So a string starting with 1 must become all
  ones, and every 0 in it costs one OR — that is the whole answer. A
  string with no 1 at all is already sorted.
  Otherwise the target is some 0...01...1, and the cost of a given
  boundary is the number of misplaced characters: a 0 that must become 1
  costs one OR, and a 1 that must become 0 costs one AND, which is
  available precisely because an earlier 1 makes some prefix AND equal 0.
  Sweeping the boundary from the first 1 to the end while maintaining
  running counts of zeros and ones on each side prices every boundary and
  keeps the cheapest. O(n) time, O(1) extra space.
"""
import sys


def solve(n: int, bits: str) -> int:
    if bits.startswith('1'):
        return sum(1 for x in bits if x == '0')
    elif '1' not in bits:
        return 0
    starting_one_idx = bits.find('1')
    zeroes_before = 0
    zeroes_after = sum(1 for idx in range(starting_one_idx, n) if bits[idx] == '0')
    ones_before = 0
    ones_after = sum(1 for idx in range(starting_one_idx, n) if bits[idx] == '1')

    split_cost = 0
    res = 2**31-1

    for idx in range(starting_one_idx, n):
        bit = bits[idx]
        if bit == '0':
            zeroes_after -= 1
            # how many ones to convert to 0 by BIT_OR and zeroes to one by BIT_AND
            # works only if there are ones before the current zero
            zero_to_one_shape = ones_before + zeroes_after
            one_to_one_shape = zeroes_before + zeroes_after + 1
            zero_to_zero_shape = ones_before + ones_after
            split_cost = min(zero_to_one_shape, one_to_one_shape, zero_to_zero_shape)
            zeroes_before += 1
        else:
            ones_after -= 1
            zero_to_one_shape = ones_before + zeroes_after
            one_to_one_shape = zeroes_before + zeroes_after
            zero_to_zero_shape = ones_before + ones_after + 1
            split_cost = min(zero_to_one_shape, one_to_one_shape, zero_to_zero_shape)
            ones_before += 1

        res = min(res, split_cost)

    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        bits = next(it).strip()
        out.append(str(solve(n, bits)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2266/problem/C)
        assert solve(4, "0011") == 0
        assert solve(4, "1000") == 3
        assert solve(5, "01000") == 1
        assert solve(8, "01001101") == 2
        assert solve(7, "0101010") == 3
        assert solve(7, "0111101") == 1
        print("2266c.py: all tests passed")
