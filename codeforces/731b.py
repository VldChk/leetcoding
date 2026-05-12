import gc
gc.disable()

def solve(n: int, teams: list[int]) -> str:
    if teams[0] > 2:
        teams[0] = 2 if teams[0] % 2 == 0 else 1
    
    is_current_discount = teams[0] == 1
    
    i = 1
    while i < len(teams):
        
        if teams[i] == 0 :
            if is_current_discount:
                return "NO"
            else:
                i += 1
                continue
        if teams[i] > 2:
            teams[i] = 2 if teams[i] % 2 == 0 else 1
        
        if is_current_discount:
            teams[i] -= 1
            is_current_discount = not is_current_discount
            continue
        else:
            if teams[i] == 2:
                i += 1
                continue
            else:
                is_current_discount = True
                i += 1
                continue
    
    return "NO" if is_current_discount else "YES"


if __name__ == '__main__':
    n = int(input().strip()) # total number of days
    
    teams = [int(i) for i in input().strip().split(' ')] # teams each day
    print(solve(n, teams))