class Solution:
    def searchTriplets(self, arr, target):
        count = 0
        arr.sort()
        for i, n in enumerate(arr):
            start_idx = i + 1
            end_idx = len(arr) - 1
            while start_idx < end_idx:
                if n + arr[start_idx] + arr[end_idx] < target:
                    count += end_idx - start_idx
                    start_idx += 1
                else:
                    end_idx -= 1

        return count
