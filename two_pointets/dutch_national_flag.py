class Solution:
    def sort(self, arr):
        start_idx = 0
        end_idx = len(arr) - 1
        while start_idx < len(arr) and arr[start_idx] == 0:
            start_idx += 1
        while end_idx >= 0 and arr[end_idx] == 2:
            end_idx -= 1
        i = start_idx
        while i <= end_idx:
            if arr[i] == 1:
                i += 1
                continue
            elif arr[i] == 0:
                arr[i], arr[start_idx] = arr[start_idx], arr[i]
                start_idx += 1
                i += 1
            else:
                arr[i], arr[end_idx] = arr[end_idx], arr[i]
                end_idx -= 1
        return arr
