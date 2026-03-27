"""
LeetCode 42: Trapping Rain Water
https://leetcode.com/problems/trapping-rain-water/

Given n non-negative integers representing an elevation map where the width of
each bar is 1, compute how much water it can trap after raining.

Time Complexity: O(n)
Space Complexity: O(1)
"""
from typing import List


class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0

        left, right = 0, len(height) - 1
        left_max, right_max = 0, 0
        water = 0

        while left < right:
            if height[left] < height[right]:
                if height[left] >= left_max:
                    left_max = height[left]
                else:
                    water += left_max - height[left]
                left += 1
            else:
                if height[right] >= right_max:
                    right_max = height[right]
                else:
                    water += right_max - height[right]
                right -= 1

        return water


# Test cases
if __name__ == "__main__":
    solution = Solution()

    # Test case 1
    assert solution.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6

    # Test case 2
    assert solution.trap([4, 2, 0, 3, 2, 5]) == 9

    # Test case 3: empty array
    assert solution.trap([]) == 0

    # Test case 4: no water can be trapped
    assert solution.trap([1, 2, 3, 4, 5]) == 0

    # Test case 5: single element
    assert solution.trap([5]) == 0

    print("All test cases passed!")
