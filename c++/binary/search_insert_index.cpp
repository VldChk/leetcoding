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