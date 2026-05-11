"""
LeetCode 1086 - High Five (Easy, Premium)
https://leetcode.com/problems/high-five/

Given a list of the scores of different students, items, where
items[i] = [ID_i, score_i] represents one score from a student with
ID_i, calculate each student's top five average.

Return the answer as an array of pairs result, where result[j] = [ID_j,
top_five_average_j] represents the student with ID_j and their top
five average. Sort result by ID_j in increasing order.

A student's top five average is calculated by taking the sum of their
top five scores and dividing it by 5 using integer division.

Solution idea:
  Per-student keep a min-heap of size up to 5 holding the top-5 scores
  seen so far. On each new score, either heappush (if heap is below
  size 5) or heapreplace (if the new score beats the smallest of the
  current top-5). Storing students in a SortedDict gives the required
  ID-ascending output for free; the average is sum(heap) // 5 since
  every heap is guaranteed to hold exactly 5 scores by the constraints.
"""
from typing import List
from sortedcontainers import SortedDict
import heapq
class Solution:
    def highFive(self, items: List[List[int]]) -> List[List[int]]:
        d = SortedDict()
        for score in items:
            if score[0] in d:
                if len(d[score[0]]) == 5:
                    if d[score[0]][0] < score[1]:
                        heapq.heapreplace(d[score[0]], score[1])
                else:
                    heapq.heappush(d[score[0]], score[1])
            else:
                d[score[0]] = [score[1]]
        return [[k, sum(v)//5] for k, v in d.items()]


if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.highFive([
        [1, 91], [1, 92], [2, 93], [2, 97], [1, 60], [2, 77],
        [1, 65], [1, 87], [1, 100], [2, 100], [2, 76],
    ]) == [[1, 87], [2, 88]]

    # Example 2
    assert s.highFive([
        [1, 100], [7, 100], [1, 100], [7, 100], [1, 100],
        [7, 100], [1, 100], [7, 100], [1, 100], [7, 100],
    ]) == [[1, 100], [7, 100]]

    print("high_five.py: all tests passed")