"""
LeetCode 929 - Unique Email Addresses (Easy)
https://leetcode.com/problems/unique-email-addresses/

Every valid email consists of a local name and a domain name,
separated by the '@' sign. Besides lowercase letters, the email may
contain one or more '.' or '+'.

For example, in "alice@leetcode.com", "alice" is the local name, and
"leetcode.com" is the domain name.

If you add periods '.' between some characters in the local name part
of an email address, mail sent there will be forwarded to the same
address without dots in the local name. Note that this rule does not
apply to domain names.

  - "alice.z@leetcode.com" and "alicez@leetcode.com" forward to the
    same email address.

If you add a plus '+' in the local name, everything after the first
plus sign will be ignored. This allows certain emails to be filtered.
Note that this rule does not apply to domain names.

  - "m.y+name@email.com" will be forwarded to "my@email.com".

Given an array of strings emails where we send one email to each
emails[i], return the number of different addresses that actually
receive mails.

Solution idea:
  Canonicalize each email: split on '@' once, strip dots from the
  local part, then drop everything from the first '+' onward. Store
  the (canonical_local, domain) tuple in a set; the answer is the
  set's size. The try/except guards against malformed inputs by
  skipping them silently (LeetCode's test inputs are well-formed
  anyway).
"""
from typing import List
class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        d: set[tuple[str, str]] = set()
        for email in emails:
            if '@' not in email:
                continue
            try:
                local_name, domain = email.split('@')
                local_name_cleaned = local_name.strip().replace('.', '').split('+')[0]
                d.add((local_name_cleaned, domain))
            except:
                continue
        return len(d)


if __name__ == "__main__":
    s = Solution()

    assert s.numUniqueEmails([
        "test.email+alex@leetcode.com",
        "test.e.mail+bob.cathy@leetcode.com",
        "testemail+david@lee.tcode.com",
    ]) == 2                                            # Example 1

    assert s.numUniqueEmails([
        "a@leetcode.com",
        "b@leetcode.com",
        "c@leetcode.com",
    ]) == 3                                            # Example 2

    print("unique_strings.py: all tests passed")