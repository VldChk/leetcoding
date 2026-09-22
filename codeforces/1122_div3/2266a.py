def solve(n: int, a_list: list[int]) -> int:
    return n - min(a_list)


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        a_list: list[int] = [int(x) for x in input().strip().split(' ')]
        print(solve(n, a_list))