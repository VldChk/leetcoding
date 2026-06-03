"""
LeetCode 68 — Text Justification (Hard)
https://leetcode.com/problems/text-justification/

Given a list of `words` and `maxWidth`, format the text so every line is exactly
`maxWidth` characters. Pack greedily (as many words per line as fit), then for
non-last lines distribute spaces between words as evenly as possible — leftover
spaces go to the left gaps first. The LAST line is left-justified: single space
between words, trailing right-pad to `maxWidth`. Single-word non-last lines are
also left-justified (no internal space to distribute).

Example (maxWidth=16):
    ["This","is","an","example","of","text","justification."] ->
    [ "This    is    an",
      "example  of text",
      "justification.  " ]

Idea — two-pointer greedy + post-flush formatting:
Walk words; while the next word still fits (`len + current_chars + gaps <= W`)
add it. On overflow flush: compute `spaces = leftover // (n-1)` and
`leftovers = leftover % (n-1)`, then for each word append `word + " "*spaces`
plus one bonus space while `leftovers > 0`. Slice `[:maxWidth]` to trim any
overshoot at the right edge. The final flush uses single-space packing.

Complexity:
    Time  O(total characters)
    Space O(output)
"""
from typing import List
class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        words = words[::-1]
        current_length = 0
        current_words = []
        res = []
        while words:
            word = words.pop()
            if len(word) + current_length + len(current_words) <= maxWidth:
                current_length += len(word)
                current_words.append(word)
            else:
                if len(current_words) > 1:
                    spaces = (maxWidth - current_length) // (len(current_words) - 1)
                    leftovers = (maxWidth - current_length) % (len(current_words) - 1)
                else:
                    spaces = maxWidth - current_length
                    leftovers = 0
                line = str()
                for c_word in current_words:
                    line += c_word
                    line += " " * spaces
                    if leftovers > 0:
                        line += " "
                        leftovers -= 1
                line = line[:maxWidth]
                res.append(line)
                current_words = []
                current_length = 0
                current_length += len(word)
                current_words.append(word)
        
        if current_words:
            line = str()
            for c_word in current_words:
                line += c_word
                line += " "
            line += " " * (maxWidth - len(line))
            line = line[:maxWidth]
            res.append(line)

        return res


if __name__ == "__main__":
    sol = Solution()

    # Example 1
    out = sol.fullJustify(
        ["This", "is", "an", "example", "of", "text", "justification."], 16
    )
    assert out == [
        "This    is    an",
        "example  of text",
        "justification.  ",
    ], out
    assert all(len(line) == 16 for line in out)

    # Example 2 — single-word lines, last line left-justified
    out = sol.fullJustify(
        ["What", "must", "be", "acknowledgment", "shall", "be"], 16
    )
    assert out == [
        "What   must   be",
        "acknowledgment  ",
        "shall be        ",
    ], out
    assert all(len(line) == 16 for line in out)

    # Example 3
    out = sol.fullJustify(
        [
            "Science", "is", "what", "we", "understand", "well", "enough",
            "to", "explain", "to", "a", "computer.", "Art", "is", "everything",
            "else", "we", "do",
        ],
        20,
    )
    assert out == [
        "Science  is  what we",
        "understand      well",
        "enough to explain to",
        "a  computer.  Art is",
        "everything  else  we",
        "do                  ",
    ], out
    assert all(len(line) == 20 for line in out)
    print("text_justification.py: all tests passed")


