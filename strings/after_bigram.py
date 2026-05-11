"""
LeetCode 1078 - Occurrences After Bigram (Easy)
https://leetcode.com/problems/occurrences-after-bigram/

Given two strings first and second, consider occurrences in some text of
the form "first second third", where second comes immediately after first,
and third comes immediately after second.

Return an array of all the words third for each occurrence of "first
second third".

(Note the LeetCode method name `findOcurrences` — single c — is preserved
exactly so this file pastes back to the platform.)

Solution idea:
  Single linear scan over the words. Maintain `minus_two` and `minus_one`
  as the previous two words. Whenever (minus_two, minus_one) == (first,
  second), the current word is a "third" — append it. Then shift the
  window forward by one word.
"""
from typing import List

class Solution:
    def findOcurrences(self, text: str, first: str, second: str) -> List[str]:
        if len(text.split(" ")) < 3:
            return []
        res = []
        minus_two = ""
        minus_one = ""
        for i, word in enumerate(text.split(" ")):
            if i < 2:
                minus_two = minus_one
                minus_one = word
                continue  # somehow, start= not always work and I am lazy to debug
            if minus_two == first and minus_one == second:
                res.append(word)

            minus_two = minus_one
            minus_one = word
        return res


if __name__ == "__main__":
    s = Solution()

    assert s.findOcurrences("alice is a good girl she is a good student",
                            "a", "good") == ["girl", "student"]      # Example 1
    assert s.findOcurrences("we will we will rock you",
                            "we", "will") == ["we", "rock"]          # Example 2

    print("after_bigram.py: all tests passed")
