"""
LeetCode 480 - Sliding Window Median (Hard)
https://leetcode.com/problems/sliding-window-median/

The median is the middle value in an ordered integer list. If the size
of the list is even, there is no middle value. So the median is the
mean of the two middle values.

You are given an integer array nums and an integer k. There is a
sliding window of size k which is moving from the very left of the
array to the very right. You can only see the k numbers in the window.
Each time the sliding window moves right by one position.

Return the median array for each window in the original array.
Answers within 10^-5 of the actual value will be accepted.

Solution idea:
  Maintain the current window as a `SortedList` (O(log k) insert/
  delete). After computing the median of the initial window, slide
  right one step at a time: take the median of the current window,
  then remove the outgoing element (`nums[i-k]`) and insert the
  incoming one (`nums[i]`). Both operations are O(log k). The median
  helper averages the two middles for even k, returns the middle for
  odd. The trailing window's median is appended after the loop.
"""
from typing import List
from sortedcontainers import SortedList

class Solution:
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        def _return_median(sorted_l: List[int]) -> float:
            if len(sorted_l) % 2 == 1:
                return float(sorted_l[len(sorted_l)// 2])
            else:
                return float(sorted_l[len(sorted_l)// 2-1] + sorted_l[len(sorted_l)// 2]) / 2
        slicing_window = SortedList(nums[:k])
        res: List[float] = []
        for i in range(k, len(nums)):
            el = nums[i]
            res.append(_return_median(slicing_window))
            slicing_window.remove(nums[i-k])
            slicing_window.add(el)
        res.append(_return_median(slicing_window))
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.medianSlidingWindow(
        [1, 3, -1, -3, 5, 3, 6, 7], 3
    ) == [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]                         # Example 1

    assert s.medianSlidingWindow(
        [1, 2, 3, 4, 2, 3, 1, 4, 2], 3
    ) == [2.0, 3.0, 3.0, 3.0, 2.0, 3.0, 2.0]                      # Example 2

    print("sliding_window_median.py: all tests passed")
