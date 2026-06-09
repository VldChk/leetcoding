"""
LeetCode 3751 — Total Waviness of Numbers in Range I (Medium)
https://leetcode.com/problems/total-waviness-of-numbers-in-range-i/

For each integer in `[num1, num2]` (inclusive), count its "wavy" digits —
each interior digit that is a strict PEAK (greater than both neighbours) or
strict VALLEY (less than both neighbours). Return the total across the range.
The first and last digits never count. Numbers with fewer than 3 digits have
waviness 0.

Examples:
    num1=120, num2=130
        120 -> "1,2,0": 2 is a peak (1<2 and 0<2)             waves = 1
        121 -> "1,2,1": 2 is a peak                            waves = 1
        130 -> "1,3,0": 3 is a peak                            waves = 1
        all others 122..129 are monotonic                      waves = 0
        total = 3
    num1=1, num2=99 -> 0   (all numbers have < 3 digits)
    num1=101, num2=101 -> 1 (valley at the 0)

Idea — direct enumeration:
The range fits the "Range I" constraints, so we just iterate each number,
convert to its digit string, and count peaks + valleys with a single pass.
The `if num2 < 100: return 0` line is a cheap early-exit: nothing below 100
has 3 digits, so the total is forced to 0.

Complexity:
    Time  O((num2 - num1 + 1) * log10(num2))
    Space O(log10(num2)) for the digit string
"""
class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        def count_waves(s: str) -> int:
            i = 1
            waves = 0
            while i < len(s) - 1:
                if s[i-1] > s[i] and s[i+1] > s[i]:
                    waves += 1
                elif s[i-1] < s[i] and s[i+1] < s[i]:
                    waves += 1
                i += 1
            return waves
        
        if num2 < 100:
            return 0
        
        res = 0
        
        for num in range(num1, num2 + 1):
            s = str(num)
            res += count_waves(s)
        
        return res


if __name__ == "__main__":
    sol = Solution()

    # Official LC sample: [120, 130] -> 3 (120, 121, 130 each contribute 1)
    assert sol.totalWaviness(120, 130) == 3
    # All under 100 -> 0
    assert sol.totalWaviness(1, 99) == 0
    # Single number, valley
    assert sol.totalWaviness(101, 101) == 1
    # Single number, no wave (monotonic)
    assert sol.totalWaviness(123, 123) == 0
    # 4-digit number with two waves: 1213 -> "1,2,1,3": 2 is a peak, 1 is a valley -> 2
    assert sol.totalWaviness(1213, 1213) == 2
    # Mixed range: 100..102
    #   100 "1,0,0" -> 0; 101 "1,0,1" -> 1 (valley); 102 "1,0,2" -> 1 (valley)
    assert sol.totalWaviness(100, 102) == 2
    print("total_waviness_in_range_1.py: all tests passed")
