from collections import Counter

def solve(n: int, m: int, a_list: list[int]) -> int:
    d = Counter(a % m for a in a_list if a % m != 0)

    mx_val = 0
    mn_key = 2**31-1

    for key, val in d.items():
        if val == mx_val:
            mn_key = min(mn_key, key)
        elif val > mx_val:
            mx_val = val
            mn_key = key

    if not d:
        return 0
    return (mx_val - 1) * m + (m-mn_key) + 1



if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n, m = map(int, input().strip().split())
        a_list = [int(x) for x in input().strip().split()]
        print(solve(n, m, a_list))