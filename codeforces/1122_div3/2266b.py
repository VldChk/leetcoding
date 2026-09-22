def solve(a_list: list[int]) -> int:
    return max(a_list[0] + a_list[2] - a_list[1], abs(a_list[0] - a_list[1]))


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        # n =  int(input().strip())
        a_list: list[int] = [int(x) for x in input().strip().split(' ')]
        print(solve(a_list))