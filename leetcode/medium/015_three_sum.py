"""
LeetCode 15: 3Sum
https://leetcode.com/problems/3sum/

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Time Complexity: O(n^2)
Space Complexity: O(1) excluding the output array
"""
from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            # Skip duplicates for the first element
            if i > 0 and nums[i] == nums[i - 1]:
                continue

            # Early termination: if smallest number is positive, no solution
            if nums[i] > 0:
                break

            left, right = i + 1, n - 1

            while left < right:
                total = nums[i] + nums[left] + nums[right]

                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])

                    # Skip duplicates for second element
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    # Skip duplicates for third element
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1

                    left += 1
                    right -= 1

        return result


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    result = solution.threeSum([-1, 0, 1, 2, -1, -4])
    assert sorted([sorted(x) for x in result]) == sorted([[-1, -1, 2], [-1, 0, 1]])

    # Test case 2
    assert solution.threeSum([0, 1, 1]) == []

    # Test case 3
    assert solution.threeSum([0, 0, 0]) == [[0, 0, 0]]

    # Test case 4: empty array
    assert solution.threeSum([]) == []

    print("All test cases passed!")
