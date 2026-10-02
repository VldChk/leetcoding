"""
Codeforces 2267A - Turn Into a Palindrome  (Round 1123, Div. 2)  [rating 800]
https://codeforces.com/contest/2267/problem/A

Ali has a string s of n lowercase letters and a fixed lowercase letter c.
For one coin he may pick any index i and overwrite s_i with c — c is the
only character he is ever allowed to write. Find the minimum number of
coins needed to make s a palindrome.

Sample (n, c, s -> coins):
  4, 'b', "abca"       -> 1      8,  'd', "adbccbad"   -> 2
  3, 'p', "xyx"        -> 0      10, 'c', "codeforces" -> 8
  5, 'e', "abcbb"      -> 2

Solution idea:
  Every mirror pair (s_i, s_{n-1-i}) is independent, and the middle
  character of an odd-length string is already a palindrome on its own.
  For one pair: if the two characters match it is free. Otherwise they
  must be made equal, and the only writable character is c — so if one
  side already equals c, overwrite the other for 1 coin; if neither does,
  the only way to agree is to write c on both, for 2 coins. Summing that
  per-pair cost is optimal because no coin can ever help two pairs at
  once. O(n) time, O(1) space.
"""
import sys


def solve(n: int, c: str, s: str)-> int:
    i = 0
    res = 0
    while i < len(s) // 2:
        if s[i] == s[n-1]:
            pass
        else:
            if s[i] == c:
                res += 1
            elif s[n-1] == c:
                res += 1
            else:
                res += 2
        i += 1
        n -= 1
    return res


def main(data: str) -> None:
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n_str, c = next(it).split()
        s = next(it).strip()
        out.append(str(solve(int(n_str), c, s)))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2267/problem/A)
        assert solve(4, 'b', "abca") == 1
        assert solve(3, 'p', "xyx") == 0
        assert solve(5, 'e', "abcbb") == 2
        assert solve(8, 'd', "adbccbad") == 2
        assert solve(10, 'c', "codeforces") == 8
        print("2267a.py: all tests passed")
