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
