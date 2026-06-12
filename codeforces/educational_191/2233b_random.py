import random
def solve(n):
    def is_valid(part_one, part_two, part_three, part_four):
        pos = [[0 for _ in range(4)] for _ in range(n)]
        for i, p in enumerate(part_one):
            pos[p-1][0] = i
        for i, p in enumerate(part_two):
            pos[p-1][1] = i
            pos[p-1][0] -= i
        for i, p in enumerate(part_three):
            pos[p-1][2] = i
            pos[p-1][1] -= i
        for i, p in enumerate(part_four):
            pos[p-1][3] = i
            pos[p-1][2] -= i
        for i in range(n):
            if pos[i][0] == pos[i][1] or pos[i][1] == pos[i][2] or pos[i][2] == pos[i][0]:
                return False
        return True

    tmp = [i for i in range(1, n+1)]
    part_one = tmp.copy()
    random.shuffle(tmp)
    part_two = tmp.copy()
    random.shuffle(tmp)
    part_three = tmp.copy()
    random.shuffle(tmp)
    part_four = tmp.copy()
    while not is_valid(part_one, part_two, part_three, part_four):
        random.shuffle(part_one)
        random.shuffle(part_two)
        random.shuffle(part_three)
        random.shuffle(part_four)
    
    res = []
    res.extend(part_one)
    res.extend(part_two)
    res.extend(part_three)
    res.extend(part_four)

    # interim = [list(i) for i in zip(part_one, part_two)]
    # part_three = [i for x_i in interim for i in x_i]
    # if n <= 3:
    #     part_five = [n-1, n] + [i for i in range(1, n-1)]
    # else:
    #     part_five = [n-2, n-1, n] + [i for i in range(1, n-2)]
    # part_three.extend(part_one)
    # part_three.extend(part_five)
    # part_one.extend(part_five)
    return ' '.join(str(i) for i in res)


if __name__ == '__main__':
    t = int(input().strip())
    for _ in range(t):
        n =  int(input().strip())
        print(solve(n))