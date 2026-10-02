from collections import defaultdict
def solve(n: int, m: int, a_list: list[int]) -> int:
    d = defaultdict(int)

    for a in a_list:
        d[a % m] += 1

    res = 0 

    for k in d:
        if k == 0:
            res += 1
            continue
        if d[k] > 0 and m - k in d and d[m - k] > 0:
            min_val = min(d[k], d[m - k])
            d[k] -= min_val
            d[m - k] -= min_val
            if d[k] > 0:
                d[k] -= 1
            elif d[m - k] > 0:
                d[m - k] -= 1
            res += 1
        
        if d[k] > 0:
            res += d[k]

    return res


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n, m = map(int, input().strip().split())
        a_list = [int(x) for x in input().strip().split()]
        print(solve(n, m, a_list))