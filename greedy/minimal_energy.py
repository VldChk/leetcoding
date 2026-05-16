"""
LeetCode 1665 - Minimum Initial Energy to Finish Tasks (Hard)
https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/

You are given an array tasks where tasks[i] = [actual_i, minimum_i]:
  * actual_i is the actual amount of energy you spend to finish the
    i-th task.
  * minimum_i is the minimum amount of energy you require to begin the
    i-th task.

For example, if the task is [10, 12] and your current energy is 11,
you cannot start this task. However, if your current energy is 13, you
can complete this task, and your energy will be 3 after finishing it.

You can finish the tasks in any order you like. Return the minimum
initial amount of energy you will need to finish all the tasks.

Solution idea:
  Greedy: sort tasks by `minimum - actual` ascending so that high-
  "leftover" tasks (those whose threshold is far above their cost)
  end up at the *end* of the sorted list. The recurrence
    res_i = max(res_{i-1} + actual_i, minimum_i)
  computes the answer "in reverse": after unrolling it equals
    max_k (minimum_k + sum_{j > k} actual_j),
  i.e. the worst constraint when tasks are *executed* with high-
  leftover ones first (= run earliest in the sorted-reverse order).
  That ordering is the classic exchange-argument optimum for this
  problem. O(n log n).
"""
from typing import List
class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        tasks.sort(key=lambda x: x[1]-x[0])
        res = tasks[0][1]
        for i in range(1, len(tasks)):
            completion, minimal = tasks[i]
            old_res = res
            res = max(old_res + completion, minimal)
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.minimumEffort([[1, 2], [2, 4], [4, 8]]) == 8                                          # Example 1
    assert s.minimumEffort([[1, 3], [2, 4], [10, 11], [10, 12], [8, 12]]) == 32                     # Example 2
    assert s.minimumEffort([[1, 7], [2, 8], [3, 9], [4, 10], [5, 11], [6, 12]]) == 27               # Example 3

    print("minimal_energy.py: all tests passed")
