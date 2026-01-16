def searchTriplets(arr):
    # bruteforce
    d = {
        tuple(sorted([arr[i], arr[j], arr[k]]))
        for i in range(len(arr))
        for j in range(len(arr))
        for k in range(len(arr))
        if i != j and i != k and k != j and arr[i] + arr[j] + arr[k] == 0
    }
    # print(d)
    triplets = [list(t) for t in d]
    return triplets



class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        nums.sort()
        triplets = set()
        # print(arr)

        for i, n in enumerate(nums):
            if i > 0 and n == nums[i-1]:
                continue
            # print(f"start for {n}")
            start_idx = i+1
            end_idx = len(nums) - 1
            target_sum = (-1) * n
            while start_idx < end_idx:
                if nums[start_idx] + nums[end_idx] > target_sum:
                    end_idx -= 1
                elif nums[start_idx] + nums[end_idx] < target_sum:
                    start_idx += 1
                else:
                    # print("Found", [arr[start_idx], arr[end_idx], n])
                    t = (n, nums[start_idx], nums[end_idx])
                    triplets.add(t)
                    start_idx += 1
                    end_idx -= 1
        return [list(t) for t in triplets]
        
        
