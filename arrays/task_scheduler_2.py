"""
LeetCode 2365 - Task Scheduler II (Medium)
https://leetcode.com/problems/task-scheduler-ii/

You are given a 0-indexed array of positive integers tasks,
representing tasks that need to be completed in order, where tasks[i]
represents the type of the i-th task.

You are also given a positive integer space, which represents the
minimum number of days that must pass after the completion of a task
before another task of the same type can be performed.

Each day, until all tasks have been completed, you must either:
  * Complete the next task from tasks, or
  * Take a break.

Return the minimum number of days needed to complete all tasks.

Solution idea:
  Linear scan over tasks, maintaining a `fq` map from task-type to the
  day on which that type was most recently completed (initialised to
  -space-1 so that the very first occurrence is always eligible).
  At each step either complete the task on the current day (cooldown
  satisfied) or skip ahead exactly the right number of idle days to
  satisfy the cooldown, then complete it. O(n) time, O(distinct
  task types) space.
"""
from typing import List

class Solution:
    def taskSchedulerII(self, tasks: List[int], space: int) -> int:
        j = 0
        ticks = 0
        fq = {t: -space-1 for t in tasks}
        while j < len(tasks):
            if ticks - fq[tasks[j]] > space:
                fq[tasks[j]] = ticks
                j += 1
                ticks += 1
            else:
                ticks += space - (ticks - fq[tasks[j]]) + 1
                fq[tasks[j]] = ticks
                j += 1
                ticks += 1
        return ticks


if __name__ == "__main__":
    s = Solution()

    assert s.taskSchedulerII([1, 2, 1, 2, 3, 1], 3) == 9      # Example 1
    assert s.taskSchedulerII([5, 8, 8, 5], 2) == 6              # Example 2

    print("task_scheduler_2.py: all tests passed")
