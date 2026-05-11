"""
LeetCode 2288 - Apply Discount to Prices (Medium)
https://leetcode.com/problems/apply-discount-to-prices/

A sentence is a string of single-space separated words where each word
can contain digits, lowercase letters, and the dollar sign '$'. A word
represents a price if it satisfies all of the following:
  - It is a sequence of digits preceded by a dollar sign '$'.
  - The number of digits is in the range [1, 10].
  - The leading digit (if there is one) is non-zero.

You are given a string sentence representing a sentence and an integer
discount. For each word representing a price, apply a discount of
discount% on the price and update the word in the sentence. All
discounted prices should be represented with exactly two decimal places.

Return a string representing the modified sentence.

Solution idea:
  Tokenize on spaces. For each word, check the price shape: starts with
  $, length > 1, and the suffix after $ is all digits. Apply discount as
  cents = price_int * (100 - discount), then format back as
  f"${cents/100:.2f}". Other words are passed through unchanged. Rejoin
  with single spaces.
"""


class Solution:
    def discountPrices(self, sentence: str, discount: int) -> str:
        keep = 100 - discount
        words = sentence.split(" ")

        for i, word in enumerate(words):
            if len(word) > 1 and word[0] == "$" and word[1:].isdigit():
                cents = int(word[1:]) * keep
                words[i] = f"${cents / 100:.2f}"

        return " ".join(words)


if __name__ == "__main__":
    s = Solution()

    # Example 1
    assert s.discountPrices(
        "there are $1 $2 and 5$ candies in the shop", 50
    ) == "there are $0.50 $1.00 and 5$ candies in the shop"

    # Example 2
    assert s.discountPrices(
        "1 2 $3 4 $5 $6 7 8$ $9 $10$", 100
    ) == "1 2 $0.00 4 $0.00 $0.00 7 8$ $0.00 $10$"

    print("apply_discount.py: all tests passed")
