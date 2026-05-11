"""
LeetCode 56 - Merge Intervals (Medium)
https://leetcode.com/problems/merge-intervals/

Given an array of intervals where intervals[i] = [start_i, end_i],
merge all overlapping intervals, and return an array of the
non-overlapping intervals that cover all the intervals in the input.

Solution idea (this implementation, sorting by end descending):
  Sort intervals by end value in descending order. Walk left to right
  with a "current group" anchored at index `j` and a running `min_start`
  for that group. For each next interval, if its end is below the
  current min_start, the groups don't overlap: emit [min_start,
  intervals[j].end] and reset the group anchor to next_j. Otherwise
  fold it into the running group by lowering min_start. After the
  scan, flush the open group. (Note: the conventional approach sorts
  by start ascending; this end-descending variant achieves the same
  result.) LeetCode accepts the merged set in any order.
"""
from typing import List
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) == 1:
            return intervals
        intervals.sort(key= lambda x: x[1], reverse=True)
        j = 0
        next_j = j + 1
        res: List[List[int]] = []
        min_start = intervals[j][0]
        while j < len(intervals) and next_j < len(intervals):
            if intervals[next_j][1] < min_start:
                res.append([min_start, intervals[j][1]])
                j = next_j
            min_start = min(min_start, intervals[next_j][0])
            next_j += 1
            
        res.append([min_start, intervals[j][1]])
        return res


if __name__ == "__main__":
    s = Solution()

    def normalize(intervals: List[List[int]]) -> List[List[int]]:
        # LC accepts any order of merged intervals; sort for comparison.
        return sorted(intervals)

    assert normalize(s.merge([[1, 3], [2, 6], [8, 10], [15, 18]])) == \
        normalize([[1, 6], [8, 10], [15, 18]])              # Example 1
    assert normalize(s.merge([[1, 4], [4, 5]])) == \
        normalize([[1, 5]])                                  # Example 2

    print("merge_intervals.py: all tests passed")
