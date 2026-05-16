"""
Codeforces 731B - Coupons and Discounts
https://codeforces.com/problemset/problem/731/B

Sereja is coaching ICPC training teams. The team will train for n
consecutive days. During day i exactly a_i different teams come, and
Sereja orders exactly one pizza per team-day (so a_i pizzas on day i,
no more no less).

He may pay only using these two promotions:
  * Discount: buy two pizzas on the *same* day for one price.
  * Coupon:   buy one pizza on day i and one pizza on day i+1 for one
              price.

He may stack as many discounts and coupons as he likes. He may not
buy more pizzas than needed, and no coupon may "stick out" past day n.

Determine whether such a purchase plan exists. Print "YES" or "NO".

Input:
  n
  a_1 a_2 ... a_n        (0 <= a_i <= 10000)

Sample cases:
  4 / 1 2 1 2            -> YES
  3 / 1 0 1              -> NO

Solution idea:
  Each "coupon" flips the parity of pizzas needed across two
  consecutive days. So a feasible plan exists iff in every maximal
  run of consecutive non-zero days the total parity is even (zeros
  reset the carry because a coupon cannot bridge a zero day).
  Implementation walks left-to-right with a single bit
  `is_current_discount` representing "an active half-coupon was opened
  yesterday and needs one more pizza today." If a zero day comes while
  that bit is set, it's NO. If the bit is set at the very end, it's
  also NO. The reductions `2 if even else 1` collapse large a_i down to
  the only thing that matters: same-day parity.
"""
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
    # Local tests against the published sample cases. These run before
    # the platform stdin block below; if you `python3.14 731b.py` from
    # the shell without piping stdin it'll still print the "OK" line
    # before stdin reads fail.
    assert solve(4, [1, 2, 1, 2]) == "YES"
    assert solve(3, [1, 0, 1]) == "NO"
    # Extra sanity checks pulled from the problem discussion
    assert solve(1, [0]) == "YES"          # nothing to buy
    assert solve(1, [2]) == "YES"          # one discount, done
    assert solve(1, [1]) == "NO"           # odd pizzas, no coupon partner
    assert solve(2, [1, 1]) == "YES"        # exactly one coupon
    print("731b.py: all tests passed")

if __name__ == '__main__':
    n = int(input().strip()) # total number of days

    teams = [int(i) for i in input().strip().split(' ')] # teams each day
    print(solve(n, teams))
