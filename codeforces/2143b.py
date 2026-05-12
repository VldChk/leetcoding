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
    t = int(input().strip()) # total number of orders
    
    while t > 0:
        n, k = (int(i) for i in input().strip().split(' '))
        # print (n, k)
        prices = [int(i) for i in input().strip().split(' ')]
        coupons = [int(i) for i in input().strip().split(' ')]
        print (solve(n, k, prices, coupons))
        t -= 1