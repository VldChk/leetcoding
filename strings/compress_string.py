from typing import List
class Solution:
    def compress(self, chars: List[str]) -> int:
        if len(chars) <= 1:
            return len(chars)
        it_pos: int = 1
        compression_pos: int = 1
        prev_ch = chars[0]
        cnt = 1
        while it_pos < len(chars):
            if chars[it_pos] == prev_ch:
                it_pos += 1
                cnt += 1
            else:
                prev_ch = chars[it_pos]                
                if cnt > 1:
                    s_cnt = str(cnt)
                    j: int = 0
                    while j < len(s_cnt):
                        chars[compression_pos] = s_cnt[j]
                        j += 1
                        compression_pos += 1
                chars[compression_pos] = prev_ch
                it_pos += 1
                cnt = 1
                compression_pos += 1
        s_cnt = str(cnt)
        j: int = 0
        if cnt > 1:
            while j < len(s_cnt):
                chars[compression_pos] = s_cnt[j]
                j += 1
                compression_pos += 1
        return compression_pos

