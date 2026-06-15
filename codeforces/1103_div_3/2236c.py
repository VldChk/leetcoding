"""
Codeforces 2236C - Omsk Programmers  (Round 1103, Div. 3)
https://codeforces.com/contest/2236/problem/C

Given three integers a, b and x, make a and b equal using the minimum
number of operations. Each operation is one of:
  * add 1 to either a or b;
  * replace a (or b) by floor(a / x).

Input: t test cases; each gives a, b, x.
Output: the minimum number of operations for each test case.

Sample:
  (1, 2, 3)  -> 1      (2, 3, 2)  -> 1
  (7, 3, 10) -> 2      (17, 3, 3) -> 3
  (10,10, 2) -> 0      (4, 7, 2)  -> 2      (1, 6, 2) -> 2

Solution idea:
  It is only ever useful to divide the larger value, and it is optimal to
  do all of its divisions first, then close the remaining gap with +1
  steps. So: while mx >= mn, divide mx by x (counting the op) and track
  the best total of (divisions used so far) + |mx - mn|; once mx drops
  below mn the cheapest finish is +(mn - mx), after which the roles swap
  and we continue until both reach 0. O(log_x(max(a, b))) per test case.
"""
def solve(a, b, x):
    # print(a, b, x)
 
    if a == b:
        return 0
    if a > b:
        mn, mx = b, a
    else:
        mn, mx = a, b
 
    op_two = 0
 
    res = mx - mn
 
    while not (mx == 0 and mn == 0):
        while mx >= mn:
            mx //= x
            op_two += 1
            res = min(res, op_two + abs(mx - mn))
            if mx == mn:
                return min(res, op_two)
        else:
            res = min(res, op_two + mn - mx)
            mx, mn = mn, mx
    return res
 
 
def main():
    n = int(input().strip())
    for _ in range(n):
        a, b, x = (int(i) for i in input().strip().split(' '))
        print(solve(a, b, x))
 
 
if __name__ == '__main__':
    # Official samples (codeforces.com/contest/2236/problem/C)
    assert solve(1, 2, 3) == 1
    assert solve(2, 3, 2) == 1
    assert solve(7, 3, 10) == 2
    assert solve(17, 3, 3) == 3
    assert solve(10, 10, 2) == 0
    assert solve(4, 7, 2) == 2
    assert solve(1, 6, 2) == 2
    print("2236c.py: all tests passed")


if __name__ == '__main__':
    main()