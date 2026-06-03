"""
LeetCode 1236 — Web Crawler (Medium, premium)
https://leetcode.com/problems/web-crawler/

Given a `startUrl` and a `HtmlParser` whose `getUrls(url)` returns links found
on a page, crawl every URL reachable from `startUrl` that is on the SAME host
(same domain extracted as `url.split('/')[2]`). Return all visited URLs in any
order. URLs are guaranteed to use `http://` with no port.

Example:
    startUrl = "http://news.yahoo.com/news/topics/"
    edges:
      news.yahoo.com/news/topics  -> [news.yahoo.com, news.yahoo.com/news]
      news.yahoo.com               -> [news.yahoo.com/north_america, sports.yahoo.com]
      ...
    -> All URLs under host "news.yahoo.com".

Idea — BFS with host filter:
Parse the host from `startUrl`. Keep a `seen` set. Pop URLs, fetch outgoing
links, filter to same-host & unseen, push to next layer. Loop until empty.

Complexity:
    Time  O(V + E) over the same-host subgraph
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
        queue = [url for url in htmlParser.getUrls(startUrl) if _extract_domain(url) == domain and url not in seen]
        while queue:
            layer = []
            while queue:
                url = queue.pop()
                if url in seen:
                    continue
                extracted = [u for u in htmlParser.getUrls(url) if _extract_domain(u) == domain and u not in seen]
                layer.extend(extracted)
                seen.add(url)
            queue.extend(layer)
        return list(seen)


if __name__ == "__main__":
    class MockHtmlParser:
        def __init__(self, graph):
            self.graph = graph
        def getUrls(self, url):
            return list(self.graph.get(url, []))

    sol = Solution()

    # Official LC sample (Example 1)
    urls_graph = {
        "http://news.yahoo.com/news/topics/": [
            "http://news.yahoo.com",
            "http://news.yahoo.com/news",
        ],
        "http://news.yahoo.com": [
            "http://news.yahoo.com/news",
            "http://news.yahoo.com/north_america",
            "http://sports.yahoo.com",  # different host -> skip
        ],
        "http://news.yahoo.com/news": ["http://news.yahoo.com/news/topics/"],
        "http://news.yahoo.com/north_america": [],
        "http://sports.yahoo.com": [],  # unreachable for our host
    }
    result = sol.crawl("http://news.yahoo.com/news/topics/", MockHtmlParser(urls_graph))
    expected = {
        "http://news.yahoo.com/news/topics/",
        "http://news.yahoo.com",
        "http://news.yahoo.com/news",
        "http://news.yahoo.com/north_america",
    }
    assert set(result) == expected, f"got {set(result)}"

    # Self-loop is harmless
    result = sol.crawl("http://x.com/", MockHtmlParser({"http://x.com/": ["http://x.com/"]}))
    assert set(result) == {"http://x.com/"}

    # No outgoing same-host links
    result = sol.crawl("http://only.com/", MockHtmlParser({"http://only.com/": ["http://other.com/"]}))
    assert set(result) == {"http://only.com/"}
    print("web_crawler.py: all tests passed")
