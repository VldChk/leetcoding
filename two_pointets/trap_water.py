from typing import List

class Solution:
    def trap(self, height: List[int]) -> int:
        start_idx = 0
        res = 0
        while start_idx < len(height) and height[start_idx] == 0:
            start_idx += 1
        
        stack: List[int] = []

        for i in range(start_idx, len(height)):
            if not stack:
                stack.append(height[i])
                continue
            
            if height[i] <= stack[-1]:
                stack.append(height[i])
            elif height[i] > stack[-1]:
                if stack[0] < height[i]:
                    while len(stack) > 1 and height[i] > stack[-1] and stack[-1] < stack[0]:
                        res += (stack[0] - stack[-1])
                        stack.pop()
                    stack = []
                    stack.append(height[i])
                else:
                    j = len(stack) - 1
                    while j > 0 and height[i] > stack[j]:
                        res += (height[i] - stack[j])
                        stack[j] = height[i]
                        j -= 1
                    stack.append(height[i])
        return res
        