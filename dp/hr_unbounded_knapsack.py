#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'unboundedKnapsack' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER k
#  2. INTEGER_ARRAY arr
#

def unboundedKnapsack(k, arr):
    if len(arr) == 0 or k < min(arr):
        return 0
    if k in arr:
        return k
    # Write your code here
    dp = [False for _ in range(k+1)]
    dp[0] = True
    for el in arr:
        for i in range(el, k+1):
            dp[i] = dp[i] or dp[i-el]
            if i == k+1 and dp[i]:
                return k
    i = k
    while i > 0 and not dp[i]:
        i -= 1
    return i


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(input().strip())
    
    for _ in range(t):

        first_multiple_input = input().rstrip().split()

        n = int(first_multiple_input[0])

        k = int(first_multiple_input[1])

        arr = list(map(int, input().rstrip().split()))

        result = unboundedKnapsack(k, arr)

        fptr.write(str(result) + '\n')

    fptr.close()
