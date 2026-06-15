"""
Codeforces 2236B - Tatar TV Show  (Round 1103, Div. 3)
https://codeforces.com/contest/2236/problem/B

You are given a binary string s of length n and an integer k. In one
operation you choose an index i (1 <= i <= n - k) and flip BOTH s[i] and
s[i + k] at the same time. Decide whether s can be turned into all
zeros.

Input: t test cases; each gives n and k, then the binary string s.
Output: "YES" or "NO" for each test case.

Sample:
  n=4 k=2 s=1010 -> YES
  n=3 k=2 s=111  -> NO
  n=3 k=3 s=111  -> NO
  n=3 k=1 s=110  -> YES
  n=1 k=1 s=1    -> NO

Solution idea:
  Each operation flips two positions that are k apart, i.e. two members
  of the same residue class modulo k. A flip changes the number of ones
  in that class by an even amount, so the parity of ones in every class
  i % k is invariant. The all-zero target has parity 0 everywhere, hence
  the answer is YES iff every residue class already holds an even number
  of ones. O(n) per test case.
"""
def solve(n, k, bits):
    cnt = [0] * k
    for i, bit in enumerate(bits):
        if bit == '1':
            cnt[i % k] ^= 1
    return 'NO' if any(cnt) else 'YES'
 
 
def main():
    t = int(input().strip())
    for _ in range(t):
        n, k = (int(i) for i in input().strip(). split(' '))
        bits = input().strip()
        print(solve(n, k, bits))
 
 
if __name__ == '__main__':
    # Official samples (codeforces.com/contest/2236/problem/B)
    assert solve(4, 2, "1010") == "YES"
    assert solve(3, 2, "111") == "NO"
    assert solve(3, 3, "111") == "NO"
    assert solve(3, 1, "110") == "YES"
    assert solve(1, 1, "1") == "NO"
    print("2236b.py: all tests passed")


if __name__ == '__main__':
    main()