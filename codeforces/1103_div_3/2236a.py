"""
Codeforces 2236A - Games on the Train  (Round 1103, Div. 3)
https://codeforces.com/contest/2236/problem/A

There are n towers with heights h_1, ..., h_n. You must add a value x_i
to every tower, where each addition satisfies 1 <= x_i <= k (so every
tower grows by at least 1). Find the minimum k for which all towers can
be made equal in height.

Input: t test cases; each gives n then the n heights h_i.
Output: the minimum k for each test case.

Sample:
  [1, 3]          -> 3
  [2, 6, 4]       -> 5
  [5, 4, 6, 6, 1] -> 6
  [3, 3, 3, 3]    -> 1

Solution idea:
  Every tower rises by at least 1, so the cheapest common target height
  is max(h) + 1: the tallest tower takes +1 and the shortest takes
  +(max - min + 1). The largest single addition needed is therefore
  max - min + 1, which is exactly the minimum feasible k. O(n) per test
  case.
"""
def solve(n):
    mn = min(n)
    mx = max(n)
    return (mx - mn) + 1
 
 
def main():
    n = int(input().strip())
    for _ in range(n):
        t = int(input().strip())
        h = [int(i) for i in input().strip().split(' ')]
        print(solve(h))
 
 
if __name__ == '__main__':
    # Official samples (codeforces.com/contest/2236/problem/A)
    assert solve([1, 3]) == 3
    assert solve([2, 6, 4]) == 5
    assert solve([5, 4, 6, 6, 1]) == 6
    assert solve([3, 3, 3, 3]) == 1
    print("2236a.py: all tests passed")


if __name__ == '__main__':
    main()