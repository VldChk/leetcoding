"""
Codeforces 2143B - Discounts
https://codeforces.com/problemset/problem/2143/B

You want to buy n products with prices a_1, a_2, ..., a_n. You can
buy product i individually (paying a_i coins) or use a discount
voucher.

There are k vouchers with sizes b_1, b_2, ..., b_k. A voucher of size
x lets you pick exactly x products and pay only for the x - 1 most
expensive of them — the cheapest one in the picked group is free.

Each product can appear in at most one discount group, even if it is
not the free one; each voucher can be used at most once; vouchers are
optional.

Compute the minimum total cost to buy all n products. (One test case
per call here; the harness loops over t test cases reading from
stdin.)

Sample shape (typical):
  n=5, k=2, prices=[3, 1, 4, 1, 5], coupons=[2, 3]   -> 9

Solution idea:
  Sort prices descending and coupons ascending. Greedy: use vouchers
  one-by-one in increasing size; each voucher covers the next
  `coupons[j]` items from the *front* (= most expensive remaining).
  Inside that group, the cheapest item — the *last* of the slice when
  prices are descending — is free, so we sum `prices[i : i+size-1]`,
  i.e. all but the last item of the slice. Whatever is left after
  all vouchers are spent (or all products are covered) is paid in
  full. Using a coupon never hurts (the free item's price is >= 0),
  so we always use every available coupon. O((n + k) log (n + k)).
"""
def solve(n: int, k: int, prices: list[int], coupons: list[int]) -> int:
    prices.sort(reverse=True)
    coupons.sort()
    i = 0
    j = 0
    to_pay = 0
    while i < n and j < k:
        num_of_products = coupons[j]
        to_pay += sum(prices[i:i+num_of_products-1])
        i += num_of_products
        j += 1

    if i == n:
        return to_pay
    else:
        to_pay += sum(prices[i:])
        return to_pay

if __name__ == '__main__':
    # Local tests with hand-constructed cases. The real platform input
    # bundles many cases on stdin (see loop below); these asserts run
    # before that and won't read stdin themselves.
    # n=5, k=2, prices [3,1,4,1,5] desc -> [5,4,3,1,1]; coupons asc [2,3].
    #   coupon 2 on [5,4] -> pay 5 (4 free)
    #   coupon 3 on [3,1,1] -> pay 3+1=4 (last 1 free)
    #   total = 9
    assert solve(5, 2, [3, 1, 4, 1, 5], [2, 3]) == 9
    # No coupons: pay full.
    assert solve(3, 0, [10, 20, 30], []) == 60
    # One huge coupon covers everything; only cheapest is free.
    assert solve(4, 1, [10, 20, 30, 40], [4]) == 90    # 40+30+20, 10 free
    # Coupons run out before products: leftover products paid in full.
    # prices desc [30,20,10]; coupon size 2 saves cheapest of [30,20] = 20.
    # Pay 30 (covered, top of group) + 10 (no coupon left) = 40.
    assert solve(3, 1, [10, 20, 30], [2]) == 40
    print("2143b.py: all tests passed")

if __name__ == '__main__':
    t = int(input().strip()) # total number of orders

    while t > 0:
        n, k = (int(i) for i in input().strip().split(' '))
        # print (n, k)
        prices = [int(i) for i in input().strip().split(' ')]
        coupons = [int(i) for i in input().strip().split(' ')]
        print (solve(n, k, prices, coupons))
        t -= 1
