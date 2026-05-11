"""
LeetCode 15 - 3Sum (Medium)
https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j],
nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] +
nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Solution idea:
  Sort first. Fix the leftmost element n at index i, skipping duplicates
  (n == nums[i-1]) so each n is processed once. For the remaining
  suffix, run two pointers (start_idx, end_idx) inward looking for
  arr[start] + arr[end] == -n. Move start right when sum is too small,
  end left when too large; on a hit add the triplet to a set (which
  also dedupes any equal-element duplicates) and advance both pointers.
"""


class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        triplets: set[tuple[int, int, int]] = set()

        for i, n in enumerate(nums):
            if i > 0 and n == nums[i-1]:
                continue
            start_idx = i+1
            end_idx = len(nums) - 1
            target_sum = (-1) * n
            while start_idx < end_idx:
                if nums[start_idx] + nums[end_idx] > target_sum:
                    end_idx -= 1
                elif nums[start_idx] + nums[end_idx] < target_sum:
                    start_idx += 1
                else:
                    t = (n, nums[start_idx], nums[end_idx])
                    triplets.add(t)
                    start_idx += 1
                    end_idx -= 1
        return [list(t) for t in triplets]


if __name__ == "__main__":
    s = Solution()

    def normalize(triplets):
        # LC accepts triplets in any order and elements within each triplet
        # in any order; normalize for comparison.
        return sorted(sorted(t) for t in triplets)

    assert normalize(s.threeSum([-1, 0, 1, 2, -1, -4])) == \
        normalize([[-1, -1, 2], [-1, 0, 1]])               # Example 1
    assert normalize(s.threeSum([0, 1, 1])) == []          # Example 2
    assert normalize(s.threeSum([0, 0, 0])) == \
        normalize([[0, 0, 0]])                              # Example 3

    print("3s.py: all tests passed")
