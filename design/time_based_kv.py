"""
LeetCode 981 - Time Based Key-Value Store (Medium)
https://leetcode.com/problems/time-based-key-value-store/

Design a time-based key-value data structure that can store multiple
values for the same key at different timestamps, and retrieve the value
at a certain timestamp.

Implement the TimeMap class:
  - TimeMap()                                         initializes object.
  - void set(String key, String value, int timestamp) stores the key
                                                       with value at
                                                       timestamp.
  - String get(String key, int timestamp)              returns the value
                                                       associated with
                                                       the largest
                                                       timestamp_prev
                                                       <= timestamp; ""
                                                       if no such value.

Constraint: all timestamps for `set` calls are strictly increasing.

Solution idea:
  Per key keep a sorted list of timestamps in `_idx[key]` and a dict
  `_map[key]` mapping timestamp -> value. `set` appends (timestamps are
  strictly increasing, so the list stays sorted). `get` binary-searches
  the timestamp list with `bisect_right` and steps back one to find the
  greatest timestamp <= the query, then dict-looks up the value.
"""
import bisect
class TimeMap:

    def __init__(self):
        self._idx = {}
        self._map = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key in self._idx:
            self._idx[key].append(timestamp)
            self._map[key][timestamp] = value
        else:
            self._idx[key] = [timestamp]
            self._map[key] = {timestamp: value}

    def get(self, key: str, timestamp: int) -> str:
        if key in self._map:
            idx = bisect.bisect_right(self._idx[key], timestamp)
            if idx > 0:
                ts = self._idx[key][idx-1]
                return self._map[key][ts]
            else:
                return ""
        else:
            return ""


if __name__ == "__main__":
    # LeetCode example 1
    tm = TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"

    print("time_based_kv.py: all tests passed")
