"""
LeetCode 621 - Task Scheduler (Medium)
https://leetcode.com/problems/task-scheduler/

Given a characters array tasks, representing the tasks a CPU needs to
do, where each letter represents a different task. Tasks could be done
in any order. Each task is done in one unit of time. For each unit of
time, the CPU could complete either one task or just be idle.

However, there is a non-negative integer n that represents the cooldown
period between two same tasks (the same letter in the array), that is
that there must be at least n units of time between any two same tasks.

Return the least number of units of time that the CPU will take to
finish all the given tasks.

Solution idea:
  Greedy with a max-heap. Bucket task counts by letter; throw the
  positive counts on a max-heap. Process in "rounds" of length n+1:
  pop up to n+1 distinct tasks (the most frequent ones available),
  decrement each remaining count and push it back. If the heap is
  empty mid-round AND we're done, only count the actual tasks done
  (no trailing idle); otherwise add the full n+1 ticks. O(N log K)
  where K = number of distinct task letters.

Note: relies on heapq.heapify_max / heappop_max / heappush_max which
become public API in Python 3.14; on 3.13 and earlier you'd need to
fall back to the private `_heappop_max` & friends (or invert keys to
use the standard min-heap).
"""
from typing import List
import heapq
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        scheduler = [0] * 26
        for t in tasks:
            scheduler[ord(t) - ord('A')] += 1
        ticks = 0
        scheduler = [i for i in scheduler if i > 0]
        heapq.heapify_max(scheduler)
        while scheduler:
            cycle = n + 1
            pending_return: list[int] = []
            task_count = 0
            while cycle > 0 and scheduler:
                task = heapq.heappop_max(scheduler)
                if task > 1:
                    pending_return.append(task-1)
                task_count += 1
                cycle -= 1
            for task in pending_return:
                heapq.heappush_max(scheduler, task)
            ticks += task_count if not scheduler else n + 1

        return ticks


if __name__ == "__main__":
    s = Solution()

    assert s.leastInterval(["A", "A", "A", "B", "B", "B"], 2) == 8        # Example 1
    assert s.leastInterval(["A", "C", "A", "B", "D", "B"], 1) == 6         # Example 2
    assert s.leastInterval(["A", "A", "A", "B", "B", "B"], 3) == 10        # Example 3

    print("task_scheduler.py: all tests passed")
