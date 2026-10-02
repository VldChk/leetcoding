from collections import Counter
def solve(n: int, a_list: list[int]) -> str:
    freq_cnt = Counter(a_list)
    freq_sorted = dict(sorted(freq_cnt.items(), key=lambda x: -x[0]))
    # print(dict(freq_sorted))
    res = []
    prefix_freq = {}
    current_mode = None
    keys = list(freq_sorted.keys())
    for i, val in enumerate(keys):
        if val not in freq_sorted:
            continue
        if freq_sorted[val] == 0:
            del freq_sorted[val]
            continue
        while freq_sorted[val] > 0:
            current_mode = val
            freq_sorted[val] -= 1
            res.append(val)
            j = i + 1
            while j < len(keys):
                if keys[j] not in freq_sorted:
                    j += 1
                    continue
                res.append(keys[j])
                freq_sorted[keys[j]] -= 1
                if freq_sorted[keys[j]] == 0:
                    del freq_sorted[keys[j]]
                j += 1
        
        
        if i == len(keys) - 1:
            while freq_sorted[val] > 0:
                res.append(val)
                freq_sorted[val] -= 1
            del freq_sorted[val]
            continue

    return " ".join(map(str, res))


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        a_list = [int(x) for x in input().strip().split()]
        print(solve(n, a_list))