#!/bin/python3
"""
HackerRank - Stock Maximize (Medium)
https://www.hackerrank.com/challenges/stockmax/problem

You know in advance the share price of a stock for the next n days.
Each day you can either buy exactly one share, sell any number of
shares you already own, or do nothing. Return the maximum profit you
can obtain with an optimal trading strategy.

The function signature is `stockmax(prices)` returning the total max
profit as an integer.

Sample cases:
  prices = [5, 3, 2]    -> 0    (monotonically decreasing, never trade)
  prices = [1, 2, 100]  -> 197  (buy day 1 @ 1, buy day 2 @ 2, sell both day 3 @ 100)
  prices = [1, 3, 1, 2] -> 3    (buy 1 sell 3, buy 1 sell 2)

Solution idea:
  Identify the "useful peaks" — every strict local maximum that is
  greater than every peak to its right (the running suprema from the
  right). Walk left to right keeping a stack of peaks ordered by
  decreasing peak height (a peak gets dropped if a taller peak appears
  later). Then walk again: at each day, sell into the next remaining
  peak's price (peaks[0]). Padding the price array with leading and
  trailing zero makes the boundary checks uniform.
"""

import os
from itertools import islice
#
# Complete the 'stockmax' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts INTEGER_ARRAY prices as parameter.
#

def stockmax(prices: list[int]) -> int:
    # Write your code here
    prices = [0] + prices + [0]
    idx = 1
    revenue = 0
    peaks = [(0, -1)]
    for i, el in enumerate(islice(prices, idx, len(prices)-1, 1), start=idx):
        if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
            while peaks and peaks[-1][1] < prices[i]:
                peaks.pop()
            peaks.append((i, prices[i]))
    # print(peaks)
    for i, el in enumerate(islice(prices, idx, len(prices)-1, 1), start=idx):
        if not peaks:
            break
        elif i == peaks[0][0]:
            peaks.pop(0)
        else:
            revenue += (max(peaks[0][1]-el, 0))
    return revenue
        

if __name__ == '__main__':
    # Local tests against the HackerRank Sample Input cases. These run
    # before the file-based harness below so they always complete even
    # if in.txt/out.txt aren't where the harness expects them.
    assert stockmax([5, 3, 2]) == 0
    assert stockmax([1, 2, 100]) == 197
    assert stockmax([1, 3, 1, 2]) == 3
    print("hr_multiple_buy_one_sell.py: all tests passed")

if __name__ == '__main__':
    fptr = open('out.txt', 'w')
    intxt = open('in.txt', 'r')

    t = int(intxt.readline().strip())

    for t_itr in range(t):
        n = int(intxt.readline().strip())

        prices = list(map(int, intxt.readline().rstrip().split()))

        result = stockmax(prices)

        fptr.write(str(result) + '\n')

    fptr.close()
    intxt.close()
