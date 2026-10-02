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


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n, c = [x for x in input().strip().split(' ')]
        n = int(n)
        s = input().strip()
        print(solve(n, c, s))