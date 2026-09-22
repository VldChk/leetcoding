def solve(a_list: list[int]) -> int:
    invariants = [(val - idx + 1) for idx, val in enumerate(a_list)]

    vals = set(invariants)

    res = 0
    for inv in invariants:
        if inv - 1 not in vals:
            next_inv = inv
            while next_inv in vals:
                next_inv += 1
            res = max(res, next_inv - inv)

    return res or 0



if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        a_list: list[int] = [int(x) for x in input().strip().split(' ')]
        print(solve(a_list))