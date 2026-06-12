def solve(n):
    res = []
    res.extend([i for i in range(1, n+1)])
    res.extend([i for i in range(1, n+1)])
    res.extend(range(2, n + 1))
    res.append(1)
    res.extend(range(1, n + 1))

    return " ".join(map(str, res))


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        print(solve(n))