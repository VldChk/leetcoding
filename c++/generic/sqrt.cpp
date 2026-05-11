// LeetCode 69 - Sqrt(x) (Easy)
// https://leetcode.com/problems/sqrtx/
//
// Given a non-negative integer x, return the square root of x rounded
// down to the nearest integer. The returned integer should be
// non-negative as well.
//
// You must not use any built-in exponent function or operator (e.g.,
// pow(x, 0.5) or x ** 0.5).
//
// Solution idea:
//   Bit-length trick to bracket the answer: floor(sqrt(x)) has at most
//   ceil(bit_length(x) / 2) bits, so the search range is
//   [2, 1 << ((bit_length+1)/2)]. Then plain integer binary search:
//   compute mid*mid (in long to avoid overflow), narrow [left, right]
//   until left > right; return right (the floor).

class Solution {
public:
    int mySqrt(int x) {
        if (x < 2) {
            return x;
        }
        int bit_length = 0;
        unsigned int temp = x;
        while (temp > 0) {
            temp >>= 1;  // Right shift by 1
            bit_length++;
        }
        unsigned int left = 2;
        unsigned int right = 1 << ((bit_length + 1) / 2);
        while (left <= right) {
            unsigned int mid = left + (right - left) / 2;
            auto t = (long) mid * mid;
            if (t > x) {
                right = mid - 1;
            } else if (t < x) {
                left = mid + 1;
            } else {
                return mid;
            }
        };
        return right;
    }
};


// ----- local tests (not part of the LeetCode submission) -----
// Build and run:
//   g++ -std=c++17 sqrt.cpp -o /tmp/sq && /tmp/sq
#include <cassert>
#include <iostream>

int main() {
    Solution s;

    assert(s.mySqrt(4) == 2);          // Example 1
    assert(s.mySqrt(8) == 2);          // Example 2: floor(2.828...) = 2

    // a couple of edges that LC also tests
    assert(s.mySqrt(0) == 0);
    assert(s.mySqrt(1) == 1);

    std::cout << "sqrt.cpp: all tests passed" << std::endl;
    return 0;
}