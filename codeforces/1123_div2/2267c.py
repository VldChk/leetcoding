from typing import Generator

def solve(n: int, x: int, a_list: list[int]) -> int:
    def _find_prime_before_x(x: int) -> Generator[int, None, None]:
        t = x
        if x <= 2:
            yield x
            return
        for num in range(2, int(x**0.5) + 2):
            if t % num == 0:
                yield num
                while t % num == 0:
                    t //= num
                if t == 1:
                    return
            else:
                continue
        yield t
        return
    
    if x == 1:
        return 0
    
    # prime_before_x = _find_prime_before_x(x)

    res = 0

    for prime in _find_prime_before_x(x):
        t = sum(a for a in a_list if a % prime == 0)
        res = max(res, t)

    return res


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n, x = map(int, input().strip().split())
        a_list = [int(x) for x in input().strip().split()]
        print(solve(n, x, a_list))