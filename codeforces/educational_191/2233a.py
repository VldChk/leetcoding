"""
Codeforces 2233A - AI Project Development  (Educational Round 191)
https://codeforces.com/contest/2233/problem/A

A project needs n lines of code. Maxim always writes x lines per hour.
Nikita writes too, and chooses one of two strategies:
  * No AI:  write at y lines per hour from the very start.
  * Use AI: spend the first z hours setting up an AI agent (writing
            nothing during that time), then write at 10*y lines/hour.
The project is done once at least n lines are written in total. Time is
counted in full hours (a partially used final hour counts as a whole
one). Output the minimum number of hours if Nikita acts optimally.

Input: t test cases; each gives n, x, y, z.
Output: the minimum number of full hours.

Sample (n x y z -> hours):
  1 1 1 1 -> 1       2 1 1 5 -> 1       3 1 1 1 -> 2
  110 10 9 1 -> 2    54 14 1 1 -> 3     30 8 1 13 -> 4
  6 2 1 3 -> 2       82 4 5 7 -> 8      200 3 2 4 -> 13
  76 211 743 432 -> 1

Solution idea:
  Compare the two strategies and take the minimum. No-AI is a constant
  x + y lines/hour, i.e. ceil(n / (x + y)) hours. The AI path is
  simulated hour by hour: every hour adds x (Maxim); for the first z
  hours Nikita is tuning (adds 0), afterwards Nikita adds 10*y. Count
  hours until the running total reaches n. O(answer) per test case.
"""
def solve(n, x, y, z):
    if n <= x:
        return 1
    elif n <= y:
        return 1
    else:
        just_code = (n // (x + y)) + (1 if n % (x + y) > 0 else 0)
        with_ai = 0
        tuning_hours = 0
        hrs = 0
        while with_ai < n:
            if tuning_hours < z:
                tuning_hours += 1
            else:
                with_ai += y*10
            with_ai += x
            hrs += 1
        return min(just_code, hrs)


if __name__ == '__main__':
    # Official samples (codeforces.com/contest/2233/problem/A)
    assert solve(1, 1, 1, 1) == 1
    assert solve(2, 1, 1, 5) == 1
    assert solve(3, 1, 1, 1) == 2
    assert solve(110, 10, 9, 1) == 2
    assert solve(54, 14, 1, 1) == 3
    assert solve(30, 8, 1, 13) == 4
    assert solve(6, 2, 1, 3) == 2
    assert solve(82, 4, 5, 7) == 8
    assert solve(200, 3, 2, 4) == 13
    assert solve(76, 211, 743, 432) == 1
    print("2233a.py: all tests passed")


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n, x, y, z = (int(i) for i in input().strip().split(' '))
        print(solve(n, x, y, z))