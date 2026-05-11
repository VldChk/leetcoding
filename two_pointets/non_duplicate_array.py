"""
LeetCode 26 - Remove Duplicates from Sorted Array (Easy)
https://leetcode.com/problems/remove-duplicates-from-sorted-array/

Given an integer array nums sorted in non-decreasing order, remove the
duplicates in-place such that each unique element appears only once.
The relative order of the elements should be kept the same.

Return k, the number of unique elements in nums. The first k elements
of nums must contain those unique elements in original order.

It does not matter what you leave beyond the first k elements.

Note: this file uses the Grokking-style standalone function name
`moveElements(arr)` rather than LeetCode's
`Solution.removeDuplicates(self, nums)`. The algorithm is identical
(in-place two-pointer rewrite); only the wrapper differs.

Solution idea:
  Read pointer scans from index 1; write pointer starts at 1 (we keep
  arr[0] as the first unique value). Whenever the read value differs
  from arr[write - 1], copy it into the write slot and bump write.
  After the scan, write equals the number of unique elements (k).
"""


def moveElements(arr):
    if not arr:
        return 0
    write_idx = 1
    for read_idx in range(1, len(arr)):
        if arr[read_idx] != arr[write_idx - 1]:
            arr[write_idx] = arr[read_idx]
            write_idx += 1
    return write_idx


if __name__ == "__main__":
    # Example 1: nums=[1,1,2] -> k=2, first two are [1,2]
    a1 = [1, 1, 2]
    k1 = moveElements(a1)
    assert k1 == 2
    assert a1[:k1] == [1, 2]

    # Example 2: nums=[0,0,1,1,1,2,2,3,3,4] -> k=5, first five are [0,1,2,3,4]
    a2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k2 = moveElements(a2)
    assert k2 == 5
    assert a2[:k2] == [0, 1, 2, 3, 4]

    print("non_duplicate_array.py: all tests passed")
