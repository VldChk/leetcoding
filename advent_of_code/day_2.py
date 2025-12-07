from typing import List
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
import os

test_input = ["11-22","95-115","998-1012","1188511880-1188511890","222220-222224","1698522-1698528","446443-446449","38593856-38593862","565653-565659","824824821-824824827","2121212118-2121212124"]

def is_valid_str(row: str) -> bool:
    if len(row) % 2 == 1:
        return True
    else:
        mid_idx = len(row) // 2
        return not row[mid_idx:] == row[:mid_idx]

def process_part_one(product_ids:List[str]):
    total_sum = 0
    for row in product_ids:
        start_pos, end_pos = tuple(row.split("-"))
        start_pos, end_pos = int(start_pos), int(end_pos)
        for i in range(start_pos, end_pos+1):
            if not is_valid_str(str(i)):
                # print(i)
                total_sum += i
    return total_sum


def factorize_number(n):
    factors = [1]
    for i in range(2, n//2 + 1):
        #print(i)
        if n % i == 0:
            factors.append(i)
    return factors


def is_valid_str_part_two(row: str) -> bool:
    if len(row) == 1:
        return True
    factors = factorize_number(len(row))
    for f in factors:
        t = [row[f*i:f*(i+1)] for i in range(0, len(row)//f)]
        if all([i==j for i in t for j in t]):
            return False
    return True


def _process_raw_input(row:str):
    total_sum = 0
    start_pos, end_pos = tuple(row.split("-"))
    start_pos, end_pos = int(start_pos), int(end_pos)
    for i in range(start_pos, end_pos+1):
        if not is_valid_str_part_two(str(i)):
            #print(i)
            total_sum += i
    return total_sum


def process_part_two_parallel(product_ids:List[str]):
    total_sum = 0
    with multiprocessing.Pool(os.cpu_count()) as p:
        total_sum = sum(p.map(_process_raw_input, product_ids))
    return total_sum
