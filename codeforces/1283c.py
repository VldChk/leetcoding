def solve(a_list: list[int]) -> str:
    s_list = [i+1 for i in range(len(a_list))]
    s_a_list = sorted(a_list)
    s_a_list = [i for i in s_a_list if i != 0]
    empty_indices = []
    j = 0
    for i, a in enumerate(s_list):
        if j < len(s_a_list) and a == s_a_list[j]:
            j += 1
        else:
            empty_indices.append(a)
    # empty_indices = empty_indices[::-1]
    # print(empty_indices)
    prev_assignment = ()
    for i, a in enumerate(a_list):
        if a == 0:
            if empty_indices[-1] == i+1:
                if len(empty_indices) < 2:
                    # repairing from the previous assignment
                    a_list[i] = prev_assignment[0]
                    a_list[prev_assignment[1]] = empty_indices[-1]
                else:
                    a_list[i] = empty_indices[-2]
                    prev_assignment = (empty_indices.pop(-2), i)
            else:
                a_list[i] = empty_indices[-1]
                prev_assignment = (empty_indices.pop(), i)
    
    return " ".join(map(str, a_list))

if __name__ == '__main__':
    t = int(input().strip())
    a_list: list[int] = [int(x) for x in input().strip().split(' ')]
    print(solve(a_list))
