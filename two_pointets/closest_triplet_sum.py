class Solution:
    def searchTriplet(self, arr, target_sum):
        arr.sort()
        closest_dist = 2**31 - 1
        closest_sum = 2**31 - 1

        for i, n in enumerate(arr):
            if i > 0 and n == arr[i - 1]:
                continue
            start_idx = i + 1
            end_idx = len(arr) - 1
            while start_idx < end_idx:
                it = n + arr[start_idx] + arr[end_idx]
                if abs(it - target_sum) <= closest_dist:
                    if abs(it - target_sum) == closest_dist:
                        closest_sum = min(closest_sum, it)
                    else:
                        closest_sum = it
                    closest_dist = abs(it - target_sum)
                if it > target_sum:
                    end_idx -= 1
                elif it < target_sum:
                    start_idx += 1
                else:
                    return target_sum
        return closest_sum
