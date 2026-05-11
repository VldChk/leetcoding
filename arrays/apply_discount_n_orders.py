
"""
LeetCode 1357 - Apply Discount Every n Orders (Medium)
https://leetcode.com/problems/apply-discount-every-n-orders/

There is a supermarket frequented by many customers. Products are
represented by two parallel integer arrays `products` and `prices`,
where the i-th product has ID `products[i]` and price `prices[i]`.

When a customer pays, their bill is represented by two parallel arrays
`product` and `amount`. The subtotal is the sum of `amount[j]` * (price
of `product[j]`) over all j.

Every n-th customer receives a discount. The discounted bill is
`subtotal * ((100 - discount) / 100)`. The counter then resets.

Implement the Cashier class:
  - Cashier(int n, int discount, int[] products, int[] prices)
  - double getBill(int[] product, int[] amount)

Solution idea:
  Build a {product_id -> price} dict in __init__ for O(1) lookup. Keep
  a running customer counter; when (counter % n == 0), scale the bill
  by (100 - discount) / 100. Bill is computed by summing amount * price
  over the current order.
"""
from typing import List

class Cashier:

    def __init__(self, n: int, discount: int, products: List[int], prices: List[int]):
        self.products: dict[int, int] = dict(zip(products, prices))
        self.keep = 100-discount
        self.curr_customer = 0
        self.n_customer = n
        

    def getBill(self, product: List[int], amount: List[int]) -> float:
        bill = 0
        c_products = dict(zip(product, amount))
        for p, a in c_products.items():
            bill += a * self.products[p]
        self.curr_customer += 1
        if self.curr_customer % self.n_customer == 0:
            bill *= self.keep
            bill /= 100.0
        return float(bill)
        


# Your Cashier object will be instantiated and called as such:
# obj = Cashier(n, discount, products, prices)
# param_1 = obj.getBill(product,amount)


if __name__ == "__main__":
    # LeetCode example: every 3rd customer gets 50% off.
    # Products [1..7] priced [100,200,300,400,300,200,100].
    c = Cashier(3, 50, [1, 2, 3, 4, 5, 6, 7], [100, 200, 300, 400, 300, 200, 100])

    assert c.getBill([1, 2], [1, 2]) == 500.0           # customer 1: 100*1+200*2
    assert c.getBill([3, 7], [10, 10]) == 4000.0        # customer 2: 300*10+100*10
    assert c.getBill([1, 2, 3, 4, 5, 6, 7],
                     [1, 1, 1, 1, 1, 1, 1]) == 800.0    # customer 3: 1600 -> 50% off
    assert c.getBill([4], [10]) == 4000.0               # customer 4: 400*10
    assert c.getBill([7, 3], [10, 10]) == 4000.0        # customer 5: 100*10+300*10
    assert c.getBill([7, 5, 3, 1, 6, 4, 2],
                     [10, 10, 10, 9, 9, 9, 7]) == 7350.0  # customer 6: 14700 -> 50% off
    assert c.getBill([2, 3, 5], [5, 3, 2]) == 2500.0    # customer 7: 200*5+300*3+300*2

    print("apply_discount_n_orders.py: all tests passed")