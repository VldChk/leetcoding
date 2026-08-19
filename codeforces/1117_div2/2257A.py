"""
Codeforces 2257A - Creating Abbreviations  (Round 1117, Div. 2)
https://codeforces.com/contest/2257/problem/A

The Beaver starts with a set S of n lowercase words and repeats this
operation m times:
  * pick a sequence of one or more words from S (repeats allowed), form
    its abbreviation — the uppercase first letters of those words, in
    order — and add that abbreviation to S as an ordinary word.
Given the n initial words and the m abbreviations that were produced (in
unknown order), decide whether some order of operations could have
produced all of them.

Sample (words / abbreviations -> answer):
  [apple grand banana great cherry good] / [AG BG CG ABC] -> YES
  [apple]                                / [AA]           -> YES
  [apple]                                / [A AA]         -> YES
  [apple avocado]                        / [B BA]         -> NO

Solution idea:
  An abbreviation begins with the first letter of its own first word, so
  adding it to S never introduces a starting letter that was not already
  available. The set of usable first letters is therefore frozen at the
  initial words, and the order of operations is irrelevant: every
  abbreviation is buildable straight from the initial words as long as
  each of its letters is the uppercased first letter of some initial
  word. Answer YES exactly when the abbreviation letters are a subset of
  those first letters. O(total input length) time and space.
"""
import sys


def solve(n, m, words, abbreviations):
    all_letters = set()
    for abbr in abbreviations:
        all_letters.update(set([_ for _ in abbr]))

    all_first_letters = set()
    for word in words:
        all_first_letters.add(word[0].upper())

    return "NO" if len(all_letters - all_first_letters) > 0 else "YES"


def main(data):
    it = iter(data.split('\n'))
    t = int(next(it))
    out = []
    for _ in range(t):
        n, m = (int(v) for v in next(it).split())
        words = [next(it).strip() for _ in range(n)]
        abbreviations = [next(it).strip() for _ in range(m)]
        out.append(solve(n, m, words, abbreviations))
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    _data = '' if sys.stdin.isatty() else sys.stdin.read()
    if _data.strip():
        main(_data)
    else:
        # Official samples (codeforces.com/contest/2257/problem/A)
        assert solve(6, 4,
                     ["apple", "grand", "banana", "great", "cherry", "good"],
                     ["AG", "BG", "CG", "ABC"]) == "YES"
        assert solve(1, 1, ["apple"], ["AA"]) == "YES"
        assert solve(1, 2, ["apple"], ["A", "AA"]) == "YES"
        assert solve(2, 2, ["apple", "avocado"], ["B", "BA"]) == "NO"
        print("2257A.py: all tests passed")
