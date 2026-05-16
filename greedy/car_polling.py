from typing import List

class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        if len(trips) == 1:
            return trips[0][0] <= capacity
        current_load = 0
        i = 0
        j = 0
        pick_ups = [(x[1], x[0]) for x in trips]
        pick_ups.sort(key=lambda x: x[0])
        drop_offs = [(x[2], x[0]) for x in trips]
        drop_offs.sort(key=lambda x: x[0])
        while i < len(pick_ups) and j < len(drop_offs):
            if current_load > capacity:
                return False
            
            if pick_ups[i][0] >= drop_offs[j][0]:
                while pick_ups[i][0] >= drop_offs[j][0]:
                    current_load -= drop_offs[j][1]
                    j += 1
            
            current_load += pick_ups[i][1]
            i += 1
        
        if i == len(pick_ups) - 1:
            return current_load <= capacity
        else:
            return (current_load + sum(x[1] for x in pick_ups[i:])) <= capacity
                
        