class Solution(object):
    def fourSum(self, nums, target):
        arr = nums
        def _find_triplets(arr, target, offset):
            triplets = []
            i = offset

            while i < len(arr) - 1:
                n = arr[i]
                if i > offset and n == arr[i-1]:
                    i += 1
                    continue
                start_idx = i + 1
                end_idx = len(arr) - 1
                while start_idx < end_idx:
                    it = n + arr[start_idx] + arr[end_idx]
                    if it - target > 0:
                        end_idx -= 1
                    elif it - target < 0:
                        start_idx += 1
                    else:
                        t = [n, arr[start_idx], arr[end_idx]]
                        triplets.append(t)
                        start_idx += 1
                        end_idx -= 1
                i += 1
            return triplets

        arr.sort()
        quadruplets = set()
        i = 0
        while i < len(arr) - 2:
            n = arr[i]
            if i > 0 and n == arr[i-1]:
                i += 1
                continue
            triplets = _find_triplets(arr, (-1) * (n - target), i + 1)
            for t in triplets:
                quadruplets.add(tuple([n] + t))
            i += 1
        return [list(q) for q in quadruplets]