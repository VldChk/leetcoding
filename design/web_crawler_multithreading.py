"""
LeetCode 1242 — Web Crawler Multithreaded (Medium, premium)
https://leetcode.com/problems/web-crawler-multithreaded/

Same crawling contract as LC 1236: start from `startUrl`, follow `HtmlParser.getUrls`
edges, stay within the same hostname, return all reachable URLs in any order.
LC's grader injects a ~15ms delay per `getUrls` call so single-threaded solutions
TLE — the point is to parallelise the I/O.

Idea — worker pool + poison-pill termination:
- A `Queue` holds URLs to expand. 16 worker threads pull from it.
- Each worker calls `getUrls(url)` (the expensive I/O) OUTSIDE the lock, then
  under a single `Lock` does seen-check, seen.add, queue.put for each new URL.
- After `q.join()` drains real work, push `None` once per worker. The workers
  see `None`, call `task_done()`, and return. A second `q.join()` confirms the
  poison-pills were consumed, then `t.join()` reaps the threads.

Why two `q.join()`s? The first ensures the BFS is done. The second guarantees
each poison was popped before we join the threads — otherwise a worker still
blocked on `q.get()` would dangle forever if poisons never reached it.

Complexity:
    Time  O(V + E) work, wall-clock ≈ work / 16 once the queue is hot
    Space O(V) for `seen`
"""
# """
# This is HtmlParser's API interface.
# You should not implement it, or speculate about its implementation
# """
#class HtmlParser(object):
#    def getUrls(self, url):
#        """
#        :type url: str
#        :rtype List[str]
#        """
from queue import Queue
import threading
from typing import List

class Solution:
    def crawl(self, startUrl: str, htmlParser: 'HtmlParser') -> List[str]:
        def _extract_domain(url: str) -> str:
            try:
                return url.split("/")[2].lower()
            except:
                return ""

        domain = _extract_domain(startUrl)

        seen = {startUrl}
        q = Queue()
        q.put(startUrl)

        lock = threading.Lock()

        def worker():
            while True:
                url = q.get()

                if url is None:
                    q.task_done()
                    return

                try:
                    for nxt in htmlParser.getUrls(url):
                        if _extract_domain(nxt) != domain:
                            continue

                        with lock:
                            if nxt not in seen:
                                seen.add(nxt)
                                q.put(nxt)
                finally:
                    q.task_done()

        threads = []
        for _ in range(16):
            t = threading.Thread(target=worker)
            t.start()
            threads.append(t)

        q.join()

        for _ in threads:
            q.put(None)

        q.join()

        for t in threads:
            t.join()

        return list(seen)


if __name__ == "__main__":
    import time

    class MockHtmlParser:
        """Simulates LC's grader: small artificial delay per call."""
        def __init__(self, graph, delay=0.005):
            self.graph = graph
            self.delay = delay
        def getUrls(self, url):
            time.sleep(self.delay)
            return list(self.graph.get(url, []))

    sol = Solution()

    # Official LC sample
    urls_graph = {
        "http://news.yahoo.com/news/topics/": [
            "http://news.yahoo.com",
            "http://news.yahoo.com/news",
        ],
        "http://news.yahoo.com": [
            "http://news.yahoo.com/news",
            "http://news.yahoo.com/north_america",
            "http://sports.yahoo.com",  # different host
        ],
        "http://news.yahoo.com/news": ["http://news.yahoo.com/news/topics/"],
        "http://news.yahoo.com/north_america": [],
        "http://sports.yahoo.com": [],
    }
    result = sol.crawl("http://news.yahoo.com/news/topics/", MockHtmlParser(urls_graph))
    expected = {
        "http://news.yahoo.com/news/topics/",
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/north_america",
    }
    assert set(result) == expected, f"got {set(result)}"

    # Self-loop
    result = sol.crawl("http://x.com/", MockHtmlParser({"http://x.com/": ["http://x.com/"]}))
    assert set(result) == {"http://x.com/"}

    # Wider graph to exercise concurrency
    graph = {f"http://a.com/{i}": [f"http://a.com/{j}" for j in range(20) if j != i]
             for i in range(20)}
    result = sol.crawl("http://a.com/0", MockHtmlParser(graph))
    assert set(result) == {f"http://a.com/{i}" for i in range(20)}
    print("web_crawler_multithreading.py: all tests passed")