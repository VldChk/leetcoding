def solve(s, k, n):
    pref_open = [0] * (n + 1)
    for i, c in enumerate(s):
        pref_open[i + 1] = pref_open[i] + (1 if c == "(" else 0)

    suff_close = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suff_close[i] = suff_close[i + 1] + (1 if s[i] == ")" else 0)

    best = n + 1
    cut = 0

    for p in range(n + 1):
        value = pref_open[p] + suff_close[p]
        if value < best:
            best = value
            cut = p

    need = min(k, best)
    ans = ["0"] * n

    for i in range(cut):
        if need > 0 and s[i] == "(":
            ans[i] = "1"
            need -= 1

    for i in range(cut, n):
        if need > 0 and s[i] == ")":
            ans[i] = "1"
            need -= 1

    return "".join(ans)


if __name__ == "__main__":
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        print(solve(s, k, n))