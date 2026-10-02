def solve(n: int, a_list: list) -> int:
    a_list.sort()
    res = 0
    curr = 0
    for a in a_list:
        curr += 1
        if curr >= a:
            res += 1
            curr = 0
    return res


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        a_list = [int(x) for x in input().strip().split()]
        print(solve(n, a_list))