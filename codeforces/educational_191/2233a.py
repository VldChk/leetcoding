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
    t = int(input().strip())
    for _ in range(t):
        n, x, y, z = (int(i) for i in input().strip().split(' '))
        print(solve(n, x, y, z))