
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