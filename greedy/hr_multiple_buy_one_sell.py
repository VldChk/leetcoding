#!/bin/python3

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
