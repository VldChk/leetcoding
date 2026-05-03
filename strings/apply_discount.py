class Solution:
    def discountPrices(self, sentence: str, discount: int) -> str:
        keep = 100 - discount
        words = sentence.split(" ")

        for i, word in enumerate(words):
            if len(word) > 1 and word[0] == "$" and word[1:].isdigit():
                cents = int(word[1:]) * keep
                words[i] = f"${cents / 100:.2f}"

        return " ".join(words)
