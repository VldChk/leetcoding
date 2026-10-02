"""
Codeforces 1703E - Mirror Grid  (Round 806, Div. 4)
https://codeforces.com/problemset/problem/1703/E

You are given an n x n grid whose cells hold 0 or 1. One operation flips a
single cell. Find the minimum number of flips that make the grid identical
to itself rotated by 0, 90, 180 and 270 degrees.

Sample (grid -> flips):
  010 / 110 / 010                          -> 1
  0                                        -> 0
  11100 / 11011 / 01011 / 10011 / 11000    -> 9
  01000 / 10101 / 01010 / 00010 / 01001    -> 7
  11001 / 00000 / 11111 / 10110 / 01111    -> 6

Solution idea:
  Rotation by 90 degrees partitions the cells into orbits of four —
  (i, j), (j, n-1-i), (n-1-i, n-1-j), (n-1-j, i) — except the centre cell
  of an odd grid, which maps to itself and is free. Rotational symmetry
  means every orbit is uniform, and the cheapest way to unify four bits is
  to flip the minority, so an orbit costs min(#zeros, #ones): 0 when all
  four already agree, 1 when three do, and 2 on a two-two split. Walk
  every cell, price its orbit from how many of its three partners match,
  then overwrite the orbit with that cell's value so it is not charged
  again. O(n^2) time, O(1) extra space.
"""
import sys


def solve(n: int, matrix: list[list[int]]) -> int:
    res = 0

    for j in range(n):
        for i in range(n):
            if n % 2 == 1 and j == n // 2 and i == n // 2:
                continue
            count = ((matrix[j][i] == matrix[n-1-j][n-1-i])
                     + (matrix[j][i] == matrix[n-1-i][j])
                     + (matrix[j][i] == matrix[i][n-1-j]))

            if count == 3:
                continue
            elif count == 2:
                # three of the four already agree: one flip unifies the orbit
                matrix[n-1-j][n-1-i] = matrix[j][i]
                matrix[n-1-i][j] = matrix[j][i]
                matrix[i][n-1-j] = matrix[j][i]
                res += 1
            elif count == 1:
                # two-two split: two flips either way
                matrix[n-1-j][n-1-i] = matrix[j][i]
                matrix[n-1-i][j] = matrix[j][i]
                matrix[i][n-1-j] = matrix[j][i]
                res += 2
            else:
                # the other three agree with each other: flip this one
                matrix[j][i] = matrix[n-1-j][n-1-i]
                res += 1

    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        matrix = [[int(ch) for ch in next(it).strip()] for _ in range(n)]
        out.append(str(solve(n, matrix)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        def _grid(rows: list[str]) -> list[list[int]]:
            return [[int(ch) for ch in row] for row in rows]

        # Official samples (codeforces.com/problemset/problem/1703/E).
        # solve() rewrites the grid in place, so build a fresh one each time.
        assert solve(3, _grid(["010", "110", "010"])) == 1
        assert solve(1, _grid(["0"])) == 0
        assert solve(5, _grid(["11100", "11011", "01011", "10011", "11000"])) == 9
        assert solve(5, _grid(["01000", "10101", "01010", "00010", "01001"])) == 7
        assert solve(5, _grid(["11001", "00000", "11111", "10110", "01111"])) == 6
        print("1703e.py: all tests passed")
