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
        
        
        