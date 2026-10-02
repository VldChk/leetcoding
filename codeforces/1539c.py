from itertools import pairwise
def solve(n: int, x: int, k: int, a_list: list) -> int:
    a_list.sort()
    fisrt_pass = 1
    gaps = []
    for a, b in pairwise(a_list):
        if b - a > x:
            fisrt_pass += 1
            gaps.append(b - a)
    
    gaps.sort()

    for gap in gaps:
        needed = (gap - 1) // x
        if k >= needed and (k - needed) >= 0:
            k -= needed
            fisrt_pass -= 1
    return fisrt_pass



if __name__ == '__main__':
    n, k, x= map(int, input().strip().split())
    a_list = [int(x) for x in input().strip().split()]
    print(solve(n, x, k, a_list))