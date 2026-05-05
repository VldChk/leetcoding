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


        