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