"""
LeetCode 2360 - Longest Cycle in a Graph (Hard)
https://leetcode.com/problems/longest-cycle-in-a-graph/

You are given a directed graph of n nodes numbered from 0 to n - 1,
where each node has at most one outgoing edge.

The graph is represented with a given 0-indexed array edges of size n,
indicating that there is a directed edge from node i to node edges[i].
If there is no outgoing edge from node i, then edges[i] == -1.

Return the length of the longest cycle in the graph. If no cycle
exists, return -1.

A cycle is a path that starts and ends at the same node.

Solution idea:
  Functional-graph traversal. Each node has at most one out-edge, so
  any path eventually terminates (in -1) or revisits a node. Process
  every node; from each unseen node, walk the chain into `seen`,
  recording the path on a stack. If the walk hits -1 or a previously-
  retired node (in `memory`), there's no new cycle along this path.
  If it hits a node already on the current stack, the cycle length is
  (stack length - index of revisited node). After processing, retire
  all path nodes into `memory` so future starts skip them.
"""


class Solution:
    def longestCycle(self, edges: list[int]) -> int:
        memory: set[int] = set()
        longest_cycle = -1
        for i, e in enumerate(edges):
            if e in memory:
                continue
            elif e == -1:
                memory.add(i)
                continue
            else:
                seen: set[int] = set()
                stack: list[int] = [i]
                seen.add(i)
                el = e
                while el > -1 and el not in memory and el not in seen:
                    stack.append(el)
                    seen.add(el)
                    el = edges[el]
                if el == -1 or el in memory:
                    memory.update(seen)
                    continue
                else:
                    idx = stack.index(el)
                    cycle_l = len(stack) - idx
                    longest_cycle = max(longest_cycle, cycle_l)
                    memory.update(seen)
        return longest_cycle


if __name__ == "__main__":
    s = Solution()

    assert s.longestCycle([3, 3, 4, 2, 3]) == 3      # Example 1: 2->4->3->2
    assert s.longestCycle([2, -1, 3, 1]) == -1       # Example 2: no cycle

    print("longest_cycle_graph.py: all tests passed")
