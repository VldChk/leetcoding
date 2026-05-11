// LeetCode 35 - Search Insert Position (Easy)
// https://leetcode.com/problems/search-insert-position/
//
// Given a sorted array of distinct integers and a target value, return
// the index if the target is found. If not, return the index where it
// would be if it were inserted in order.
//
// You must write an algorithm with O(log n) runtime complexity.
//
// Solution idea:
//   Standard recursive binary search over [start_idx, end_idx). When
//   start == end, the target is missing and that index is exactly where
//   it would be inserted to preserve order. Otherwise compare nums[mid]
//   to target and recurse into the half that would contain it.

#include <vector>

class Solution {
public:
    int recursiveSearch(std::vector<int>& nums, int& start_idx, int& end_idx, int& target) {
        if (start_idx == end_idx) {
            return start_idx;
        }
        int mid_idx = (start_idx + end_idx) / 2;
        if (nums[mid_idx] > target) {
            return recursiveSearch(nums, start_idx, mid_idx, target);
        } else if (nums[mid_idx] < target) {
            int mid_start_idx = mid_idx + 1;
            return recursiveSearch(nums, mid_start_idx, end_idx, target);
        } else {
            return mid_idx;
        }
    }
    int searchInsert(std::vector<int>& nums, int target) {
        int start_idx = 0;
        int end_idx = nums.size();
        return recursiveSearch(nums, start_idx, end_idx, target);

    }
};


// ----- local tests (not part of the LeetCode submission) -----
// Build and run:
//   g++ -std=c++17 search_insert_index.cpp -o /tmp/sii && /tmp/sii
#include <cassert>
#include <iostream>

int main() {
    Solution s;

    // Example 1: target found at index 2
    {
        std::vector<int> nums = {1, 3, 5, 6};
        assert(s.searchInsert(nums, 5) == 2);
    }
    // Example 2: 2 would go before 3 -> index 1
    {
        std::vector<int> nums = {1, 3, 5, 6};
        assert(s.searchInsert(nums, 2) == 1);
    }
    // Example 3: 7 would go past the end -> index 4
    {
        std::vector<int> nums = {1, 3, 5, 6};
        assert(s.searchInsert(nums, 7) == 4);
    }

    std::cout << "search_insert_index.cpp: all tests passed" << std::endl;
    return 0;
}