def solve(n: int, bits: str) -> int:
    if bits.startswith('1'):
        return sum(1 for x in bits if x == '0')
    elif '1' not in bits:
        return 0
    starting_one_idx = bits.find('1')
    zeroes_before = 0
    zeroes_after = sum(1 for idx in range(starting_one_idx, n) if bits[idx] == '0')
    ones_before = 0
    ones_after = sum(1 for idx in range(starting_one_idx, n) if bits[idx] == '1')

    split_cost = 0
    res = 2**31-1

    for idx in range(starting_one_idx, n):
        bit = bits[idx]
        if bit == '0':
            zeroes_after -= 1
            # how many ones to convert to 0 by BIT_OR and zeroes to one by BIT_AND
            # works only if there are ones before the current zero
            zero_to_one_shape = ones_before + zeroes_after
            one_to_one_shape = zeroes_before + zeroes_after + 1
            zero_to_zero_shape = ones_before + ones_after
            split_cost = min(zero_to_one_shape, one_to_one_shape, zero_to_zero_shape)
            zeroes_before += 1
        else:
            ones_after -= 1
            zero_to_one_shape = ones_before + zeroes_after
            one_to_one_shape = zeroes_before + zeroes_after
            zero_to_zero_shape = ones_before + ones_after + 1
            split_cost = min(zero_to_one_shape, one_to_one_shape, zero_to_zero_shape)
            ones_before += 1
        
        res = min(res, split_cost)

    return res


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        bits = input().strip()
        print(solve(n, bits))