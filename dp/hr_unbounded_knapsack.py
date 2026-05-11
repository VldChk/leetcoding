#!/bin/python3
"""
HackerRank - Knapsack ("Unbounded Knapsack") (Medium)
https://www.hackerrank.com/challenges/unbounded-knapsack/problem

Given an array of integers and a target sum, determine the sum nearest
to but not exceeding the target that can be created. To create the sum,
use any element of your array zero or more times.

The function signature is `unboundedKnapsack(k, arr)` returning an
integer.

Sample cases:
  k=12, arr=[1, 6, 9]      -> 12  (e.g. 6 + 6)
  k=9,  arr=[3, 4, 4, 4, 8] -> 9   (3 + 3 + 3, or 4 + 4 doesn't fit twice)

Solution idea:
  Subset-sum DP with reuse. dp[i] = True if some unbounded combination
  of arr sums exactly to i; seed dp[0] = True. For each element `el`,
  sweep i from el up to k and set dp[i] |= dp[i - el]. After all
  elements are processed, walk down from k to find the highest True
  index — that's the closest achievable sum not exceeding k. Two
  shortcuts up front: empty arr or k < min(arr) -> 0; k itself in arr
  -> return k immediately (saves a full pass).
"""

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
    # Local tests against the HackerRank Sample Input cases. These run
    # before the platform's stdin/OUTPUT_PATH boilerplate below so they
    # complete even when this script is executed outside the HR judge.
    assert unboundedKnapsack(12, [1, 6, 9]) == 12
    assert unboundedKnapsack(9, [3, 4, 4, 4, 8]) == 9
    print("hr_unbounded_knapsack.py: all tests passed")

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
