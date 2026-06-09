"""
LeetCode 271 — Encode and Decode Strings (Medium, Premium)
https://leetcode.com/problems/encode-and-decode-strings/

Design `encode(List[str]) -> str` and `decode(str) -> List[str]` such that
`decode(encode(strs)) == strs` for any input list. No built-in
serialization libraries allowed.

Examples:
    encode(["Hello", "World"])     -> ".. (any encoding) .."
    decode(encode(["", "abc", ""])) -> ["", "abc", ""]

Idea — space-as-delimiter with a sentinel escape:
Use the literal token "<space>" as an escape so that single spaces inside
words don't collide with the " " separator used to glue the words together.
    encode: replace " " with "<space>" inside each word, then join with " ".
    decode: split on " ", then replace "<space>" with " " inside each piece.

Trade-off: this fails if the input itself ever contains the literal substring
"<space>" — that's a known limitation of the sentinel-escape approach. The
classic bullet-proof alternative is length-prefix framing ("5#hello3#abc"),
which has no forbidden substrings. The sentinel approach is simpler and
passes LC's published cases.

Complexity:
    Time  O(total characters) for both encode and decode
    Space O(total characters) for the output
"""
from typing import List
class Codec:
    def encode(self, strs: List[str]) -> str:
        """Encodes a list of strings to a single string.
        """
        return " ".join([st.replace(" ", "<space>") for st in strs])
        

    def decode(self, s: str) -> List[str]:
        """Decodes a single string to a list of strings.
        """
        return [st.replace("<space>", " ") for st in s.split(" ")]
        


# Your Codec object will be instantiated and called as such:
# codec = Codec()
# codec.decode(codec.encode(strs))


if __name__ == "__main__":
    codec = Codec()

    # Official LC sample 1
    strs = ["Hello", "World"]
    assert codec.decode(codec.encode(strs)) == strs

    # Official LC sample 2 — empty list... actually LC's sample 2 is [""]
    strs = [""]
    assert codec.decode(codec.encode(strs)) == strs

    # All empty strings
    strs = ["", "", ""]
    assert codec.decode(codec.encode(strs)) == strs

    # Strings with embedded spaces
    strs = ["hello world", "foo bar baz", "single"]
    assert codec.decode(codec.encode(strs)) == strs

    # Mixed empty / non-empty
    strs = ["", "a", "", "b", ""]
    assert codec.decode(codec.encode(strs)) == strs

    # Punctuation, mixed casing
    strs = ["abc,def", "PUNCT!", "100%"]
    assert codec.decode(codec.encode(strs)) == strs

    print("encode_decode.py: all tests passed")
