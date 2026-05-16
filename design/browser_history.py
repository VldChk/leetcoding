"""
LeetCode 1472 - Design Browser History (Medium)
https://leetcode.com/problems/design-browser-history/

You have a browser of one tab where you start on the homepage and you
can visit another url, get back in the history number of steps or move
forward in the history number of steps.

Implement the BrowserHistory class:
  * BrowserHistory(string homepage) — initialises browser with homepage.
  * void visit(string url) — visits url from current page. It clears
    all the forward history.
  * string back(int steps) — Move steps back in history. If you can
    only return x < steps in the history, return the last url that
    can be reached.
  * string forward(int steps) — Move steps forward in history. If you
    can only return x < steps forward in the history, return the
    last url that can be reached.

Solution idea:
  Stack + current pointer. `stack` holds all URLs that are currently
  reachable (the homepage plus everything visited since the last
  branch). `current_pos` is the index into `stack`. visit truncates
  any forward history past `current_pos` then appends and advances.
  back/forward clamp the new position into [0, len(stack)-1]. O(steps)
  for visit's truncation in the worst case, O(1) for back/forward.
"""
class BrowserHistory:

    def __init__(self, homepage: str):
        self.stack: list[str] = [homepage]
        self.current_pos = 0


    def visit(self, url: str) -> None:
        _d = self.current_pos
        _s = self.stack
        while len(self.stack) > self.current_pos + 1:
            self.stack.pop()
        self.stack.append(url)
        self.current_pos += 1


    def back(self, steps: int) -> str:
        _d = self.current_pos
        _s = self.stack
        self.current_pos = max(self.current_pos-steps, 0)
        return self.stack[self.current_pos]


    def forward(self, steps: int) -> str:
        _d = self.current_pos
        _s = self.stack
        self.current_pos = min(len(self.stack)-1, self.current_pos + steps)
        return self.stack[self.current_pos]



# Your BrowserHistory object will be instantiated and called as such:
# obj = BrowserHistory(homepage)
# obj.visit(url)
# param_2 = obj.back(steps)
# param_3 = obj.forward(steps)

if __name__ == "__main__":
    # Example 1 from the problem
    bh = BrowserHistory("leetcode.com")
    bh.visit("google.com")
    bh.visit("facebook.com")
    bh.visit("youtube.com")
    assert bh.back(1) == "facebook.com"
    assert bh.back(1) == "google.com"
    assert bh.forward(1) == "facebook.com"
    bh.visit("linkedin.com")           # clears forward history
    assert bh.forward(2) == "linkedin.com"   # already at top
    assert bh.back(2) == "google.com"
    assert bh.back(7) == "leetcode.com"      # clamps to homepage

    print("browser_history.py: all tests passed")
