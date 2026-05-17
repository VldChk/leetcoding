# leetcoding

A personal grind log of competitive-programming and interview-prep solutions
— mostly LeetCode, plus a sprinkling of HackerRank and Codeforces.

## File layout convention

Each task lives in its own self-contained file under a topic directory
(`arrays/`, `dp/`, `two_pointets/`, …). Every file follows the same shape:

1. **Top-of-file docstring** with the problem URL, the full statement,
   sample cases, and a short "Solution idea" paragraph explaining the
   chosen approach.
2. **The solution itself** — for LeetCode that means a top-level
   `class Solution:` with the exact method signature the platform
   expects, so the file can be pasted back into leetcode.com unchanged.
   Multi-method "design" problems keep their problem-specific class
   name (e.g. `LRUCache`, `BrowserHistory`, `Trie`) under `design/`.
3. **A small `if __name__ == "__main__":` block** with two or three
   asserts taken from the problem's own published sample cases, so you
   can run a single file and immediately see "all tests passed".

HackerRank files (`hr_*.py`) and Codeforces files (`codeforces/*.py`)
keep the platform-specific I/O harness (stdin/`OUTPUT_PATH`) intact and
add the local-test block *before* it.

## Toolchain

- **Python 3.14** for everything under `.py`. A handful of solutions
  rely on the public `heapq.heapify_max` / `heappop_max` / `heappush_max`
  API that was promoted from private underscore-prefixed helpers in 3.14,
  so older interpreters will not work.
- **C++17** for the three files under `c++/`. Each is a standalone
  translation unit in LeetCode's `class Solution { public: ... };`
  shape; build with any reasonably modern compiler (`g++ -std=c++17`).

Running a single solution:

```bash
python3.14 arrays/koko_eats_bananas.py
# -> koko_eats_bananas.py: all tests passed
```

The package under `src/pandas_dataset_generator/` is unrelated to the
practice files; see `CLAUDE.md` and `plan.md` for that.

## Stats

| Topic            | Easy | Medium | Hard | Total |
|------------------|-----:|-------:|-----:|------:|
| arrays           |    3 |     17 |    0 |    20 |
| backtrace        |    0 |      1 |    0 |     1 |
| c++              |    2 |      1 |    0 |     3 |
| codeforces       |    — |      — |    — |     2 |
| design           |    0 |      8 |    3 |    11 |
| dp               |    1 |      7 |    2 |    10 |
| graphs           |    0 |      1 |    1 |     2 |
| greedy           |    2 |      6 |    1 |     9 |
| heaps            |    1 |      1 |    1 |     3 |
| linked_lists     |    1 |      0 |    0 |     1 |
| stacks           |    0 |      3 |    1 |     4 |
| strings          |    5 |     12 |    0 |    17 |
| trees            |    2 |      1 |    0 |     3 |
| two_pointets     |    5 |     12 |    1 |    18 |
| **TOTAL**        | **22** | **70** | **10** | **104** |

- 104 solution files covering 98 distinct problems (5 problems have an
  alternate solution under a different name — usually a faster/cleaner
  re-derivation: LC 1, LC 15, LC 146, LC 238, LC 1208; LC 146 has three
  variants — two Python and one C++).
- 100 LeetCode, 2 HackerRank, 2 Codeforces.
- HackerRank entries are listed as "Medium" for stats purposes
  (HackerRank uses its own tagging; both included here are listed
  Medium on the platform).
- Codeforces problems do not have a fixed difficulty label, only a
  per-round letter, so they are excluded from the difficulty
  distribution.

## Problem index

### Arrays

- LC 33 — [Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/) (Medium) — `arrays/search_in_rotated_array.py`
- LC 59 — [Spiral Matrix II](https://leetcode.com/problems/spiral-matrix-ii/) (Medium) — `arrays/spatial_matrix_2.py`
- LC 73 — [Set Matrix Zeroes](https://leetcode.com/problems/set-matrix-zeroes/) (Medium) — `arrays/set_matrix_zeroes.py`
- LC 118 — [Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/) (Easy) — `arrays/pascal_triangle.py`
- LC 119 — [Pascal's Triangle II](https://leetcode.com/problems/pascals-triangle-ii/) (Easy) — `arrays/pascal_triangle_2.py`
- LC 153 — [Find Minimum in Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) (Medium) — `arrays/min_in_rotated_array.py`
- LC 162 — [Find Peak Element](https://leetcode.com/problems/find-peak-element/) (Medium) — `arrays/find_peak_element.py`
- LC 200 — [Number of Islands](https://leetcode.com/problems/number-of-islands/) (Medium) — `arrays/find_islands.py`
- LC 238 — [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) (Medium) — `arrays/product_except_self_fast.py`, `arrays/product_except_self_slow.py`
- LC 287 — [Find the Duplicate Number](https://leetcode.com/problems/find-the-duplicate-number/) (Medium) — `arrays/find_duplicative_number.py`
- LC 442 — [Find All Duplicates in an Array](https://leetcode.com/problems/find-all-duplicates-in-an-array/) (Medium) — `arrays/find_all_duplicates.py`
- LC 621 — [Task Scheduler](https://leetcode.com/problems/task-scheduler/) (Medium) — `arrays/task_scheduler.py`
- LC 875 — [Koko Eating Bananas](https://leetcode.com/problems/koko-eating-bananas/) (Medium) — `arrays/koko_eats_bananas.py`
- LC 973 — [K Closest Points to Origin](https://leetcode.com/problems/k-closest-points-to-origin/) (Medium) — `arrays/k_closest_origin.py`
- LC 1357 — [Apply Discount Every n Orders](https://leetcode.com/problems/apply-discount-every-n-orders/) (Medium) — `arrays/apply_discount_n_orders.py`
- LC 1605 — [Find Valid Matrix Given Row and Column Sums](https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/) (Medium) — `arrays/reconstruct_matrix.py`
- LC 2221 — [Find Triangular Sum of an Array](https://leetcode.com/problems/find-triangular-sum-of-an-array/) (Medium) — `arrays/triangular_sum.py`
- LC 2365 — [Task Scheduler II](https://leetcode.com/problems/task-scheduler-ii/) (Medium) — `arrays/task_scheduler_2.py`
- LC 2951 — [Find the Peaks](https://leetcode.com/problems/find-the-peaks/) (Easy) — `arrays/find_peaks.py`

### Backtracking

- LC 78 — [Subsets](https://leetcode.com/problems/subsets/) (Medium) — `backtrace/subsets.py`

### C++

- LC 35 — [Search Insert Position](https://leetcode.com/problems/search-insert-position/) (Easy) — `c++/binary/search_insert_index.cpp`
- LC 69 — [Sqrt(x)](https://leetcode.com/problems/sqrtx/) (Easy) — `c++/generic/sqrt.cpp`
- LC 146 — [LRU Cache](https://leetcode.com/problems/lru-cache/) (Medium) — `c++/design/lru_cache.cpp`

### Codeforces

- CF 731B — [Coupons and Discounts](https://codeforces.com/problemset/problem/731/B) — `codeforces/731b.py`
- CF 2143B — [Discounts](https://codeforces.com/problemset/problem/2143/B) — `codeforces/2143b.py`

### Design

- LC 146 — [LRU Cache](https://leetcode.com/problems/lru-cache/) (Medium) — `design/lru_cache.py`, `design/lru_cache_dict.py`
- LC 155 — [Min Stack](https://leetcode.com/problems/min-stack/) (Medium) — `design/min_stack.py`
- LC 208 — [Implement Trie (Prefix Tree)](https://leetcode.com/problems/implement-trie-prefix-tree/) (Medium) — `design/trie.py`
- LC 295 — [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) (Hard) — `design/median_of_stream.py`
- LC 380 — [Insert Delete GetRandom O(1)](https://leetcode.com/problems/insert-delete-getrandom-o1/) (Medium) — `design/random_set.py`
- LC 381 — [Insert Delete GetRandom O(1) - Duplicates allowed](https://leetcode.com/problems/insert-delete-getrandom-o1-duplicates-allowed/) (Hard) — `design/random_set_duplicate.py`
- LC 480 — [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) (Hard) — `design/sliding_window_median.py`
- LC 981 — [Time Based Key-Value Store](https://leetcode.com/problems/time-based-key-value-store/) (Medium) — `design/time_based_kv.py`
- LC 1472 — [Design Browser History](https://leetcode.com/problems/design-browser-history/) (Medium) — `design/browser_history.py`
- LC 2034 — [Stock Price Fluctuation](https://leetcode.com/problems/stock-price-fluctuation/) (Medium) — `design/stock_price.py`

### Dynamic Programming

- LC 62 — [Unique Paths](https://leetcode.com/problems/unique-paths/) (Medium) — `dp/unique_paths_1.py`
- LC 70 — [Climbing Stairs](https://leetcode.com/problems/climbing-stairs/) (Easy) — `dp/climb_stairs.py`
- LC 123 — [Best Time to Buy and Sell Stock III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) (Hard) — `dp/best_buy_and_sell_stocks_3.py`
- LC 188 — [Best Time to Buy and Sell Stock IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) (Hard) — `dp/best_buy_and_sell_stocks_4.py`
- LC 309 — [Best Time to Buy and Sell Stock with Cooldown](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) (Medium) — `dp/best_buy_sell_stocks_cooldown.py`
- LC 322 — [Coin Change](https://leetcode.com/problems/coin-change/) (Medium) — `dp/coin_change.py`
- LC 518 — [Coin Change II](https://leetcode.com/problems/coin-change-ii/) (Medium) — `dp/coin_change_2.py`
- LC 714 — [Best Time to Buy and Sell Stock with Transaction Fee](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) (Medium) — `dp/max_profit_with_transaction_fee.py`
- LC 2291 — [Maximum Profit From Trading Stocks](https://leetcode.com/problems/maximum-profit-from-trading-stocks/) (Medium, Premium) — `dp/max_profit_trading_stocks.py`
- HR — [Unbounded Knapsack](https://www.hackerrank.com/challenges/unbounded-knapsack/problem) (Medium) — `dp/hr_unbounded_knapsack.py`

### Graphs

- LC 133 — [Clone Graph](https://leetcode.com/problems/clone-graph/) (Medium) — `graphs/clone_graph.py`
- LC 2360 — [Longest Cycle in a Graph](https://leetcode.com/problems/longest-cycle-in-a-graph/) (Hard) — `graphs/longest_cycle_graph.py`

### Greedy

- LC 56 — [Merge Intervals](https://leetcode.com/problems/merge-intervals/) (Medium) — `greedy/merge_intervals.py`
- LC 121 — [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) (Easy) — `greedy/buy_and_sell_stock.py`
- LC 122 — [Best Time to Buy and Sell Stock II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) (Medium) — `greedy/buy_and_sell_stock_2.py`
- LC 202 — [Happy Number](https://leetcode.com/problems/happy-number/) (Easy) — `greedy/happy_number.py`
- LC 781 — [Rabbits in Forest](https://leetcode.com/problems/rabbits-in-forest/) (Medium) — `greedy/count_rabbits.py`
- LC 1094 — [Car Pooling](https://leetcode.com/problems/car-pooling/) (Medium) — `greedy/car_polling.py`
- LC 1665 — [Minimum Initial Energy to Finish Tasks](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/) (Hard) — `greedy/minimal_energy.py`
- LC 2457 — [Minimum Addition to Make Integer Beautiful](https://leetcode.com/problems/minimum-addition-to-make-integer-beautiful/) (Medium) — `greedy/min_added_to_beauty.py`
- HR — [Stock Maximize](https://www.hackerrank.com/challenges/stockmax/problem) (Medium) — `greedy/hr_multiple_buy_one_sell.py`

### Heaps

- LC 239 — [Sliding Window Maximum](https://leetcode.com/problems/sliding-window-maximum/) (Hard) — `heaps/max_sliding_window.py`
- LC 347 — [Top K Frequent Elements](https://leetcode.com/problems/top-k-frequent-elements/) (Medium) — `heaps/top_k_freq.py`
- LC 1086 — [High Five](https://leetcode.com/problems/high-five/) (Easy, Premium) — `heaps/high_five.py`

### Linked Lists

- LC 83 — [Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) (Easy) — `linked_lists/remove_duplicates_sorted.py`

### Stacks

- LC 150 — [Evaluate Reverse Polish Notation](https://leetcode.com/problems/evaluate-reverse-polish-notation/) (Medium) — `stacks/reverse_polish_notation.py`
- LC 739 — [Daily Temperatures](https://leetcode.com/problems/daily-temperatures/) (Medium) — `stacks/daily_temperature.py`
- LC 1106 — [Parsing A Boolean Expression](https://leetcode.com/problems/parsing-a-boolean-expression/) (Hard) — `stacks/parsing_boolean_expr.py`
- LC 1249 — [Minimum Remove to Make Valid Parentheses](https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/) (Medium) — `stacks/remove_brackets.py`

### Strings

- LC 9 — [Palindrome Number](https://leetcode.com/problems/palindrome-number/) (Easy) — `strings/palindrome.py`
- LC 17 — [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) (Medium) — `strings/letter_combinatorics_phn.py`
- LC 43 — [Multiply Strings](https://leetcode.com/problems/multiply-strings/) (Medium) — `strings/multiply_string.py`
- LC 49 — [Group Anagrams](https://leetcode.com/problems/group-anagrams/) (Medium) — `strings/group_anagrams.py`
- LC 394 — [Decode String](https://leetcode.com/problems/decode-string/) (Medium) — `strings/decode_strings.py`
- LC 415 — [Add Strings](https://leetcode.com/problems/add-strings/) (Easy) — `strings/add_strings.py`
- LC 443 — [String Compression](https://leetcode.com/problems/string-compression/) (Medium) — `strings/compress_string.py`
- LC 541 — [Reverse String II](https://leetcode.com/problems/reverse-string-ii/) (Easy) — `strings/reverse_string_k.py`
- LC 648 — [Replace Words](https://leetcode.com/problems/replace-words/) (Medium) — `strings/replace_word.py`
- LC 929 — [Unique Email Addresses](https://leetcode.com/problems/unique-email-addresses/) (Easy) — `strings/unique_strings.py`
- LC 1078 — [Occurrences After Bigram](https://leetcode.com/problems/occurrences-after-bigram/) (Easy) — `strings/after_bigram.py`
- LC 1087 — [Brace Expansion](https://leetcode.com/problems/brace-expansion/) (Medium, Premium) — `strings/brace_expansion.py`
- LC 1208 — [Get Equal Substrings Within Budget](https://leetcode.com/problems/get-equal-substrings-within-budget/) (Medium) — `strings/budget_replace.py`, `strings/budget_substring_replace.py`
- LC 2288 — [Apply Discount to Prices](https://leetcode.com/problems/apply-discount-to-prices/) (Medium) — `strings/apply_discount.py`
- LC 2390 — [Removing Stars From a String](https://leetcode.com/problems/removing-stars-from-a-string/) (Medium) — `strings/replace_stars.py`
- LC 3167 — [Better Compression of String](https://leetcode.com/problems/better-compression-of-string/) (Medium) — `strings/better_compression.py`

### Trees

- LC 111 — [Minimum Depth of Binary Tree](https://leetcode.com/problems/minimum-depth-of-binary-tree/) (Easy) — `trees/minimum_depth.py`
- LC 222 — [Count Complete Tree Nodes](https://leetcode.com/problems/count-complete-tree-nodes/) (Easy) — `trees/count_complete_tree_nodes.py`
- LC 450 — [Delete Node in a BST](https://leetcode.com/problems/delete-node-in-a-bst/) (Medium) — `trees/detele_node_bst.py`

### Two Pointers

- LC 1 — [Two Sum](https://leetcode.com/problems/two-sum/) (Easy) — `two_pointets/2s_classic.py`, `two_pointets/2s_unorthodox.py`
- LC 11 — [Container With Most Water](https://leetcode.com/problems/container-with-most-water/) (Medium) — `two_pointets/max_area.py`
- LC 15 — [3Sum](https://leetcode.com/problems/3sum/) (Medium) — `two_pointets/3s.py`, `two_pointets/zero_sum_triplets.py`
- LC 16 — [3Sum Closest](https://leetcode.com/problems/3sum-closest/) (Medium) — `two_pointets/closest_triplet_sum.py`
- LC 18 — [4Sum](https://leetcode.com/problems/4sum/) (Medium) — `two_pointets/4s.py`
- LC 26 — [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/) (Easy) — `two_pointets/non_duplicate_array.py`
- LC 42 — [Trapping Rain Water](https://leetcode.com/problems/trapping-rain-water/) (Hard) — `two_pointets/trap_water.py`
- LC 75 — [Sort Colors](https://leetcode.com/problems/sort-colors/) (Medium) — `two_pointets/dutch_national_flag.py`
- LC 167 — [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) (Medium) — `two_pointets/two_sum_sorted.py`
- LC 170 — [Two Sum III - Data structure design](https://leetcode.com/problems/two-sum-iii-data-structure-design/) (Easy, Premium) — `two_pointets/two_sum_ds.py`
- LC 259 — [3Sum Smaller](https://leetcode.com/problems/3sum-smaller/) (Medium, Premium) — `two_pointets/triplets_with_smaller_sum.py`
- LC 532 — [K-diff Pairs in an Array](https://leetcode.com/problems/k-diff-pairs-in-an-array/) (Medium) — `two_pointets/k_diff_pairs.py`
- LC 844 — [Backspace String Compare](https://leetcode.com/problems/backspace-string-compare/) (Easy) — `two_pointets/backspaced_strings.py`
- LC 1679 — [Max Number of K-Sum Pairs](https://leetcode.com/problems/max-number-of-k-sum-pairs/) (Medium) — `two_pointets/k_sum_pairs.py`
- LC 1711 — [Count Good Meals](https://leetcode.com/problems/count-good-meals/) (Medium) — `two_pointets/good_meal_count.py`
- LC 2491 — [Divide Players Into Teams of Equal Skill](https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/) (Medium) — `two_pointets/divide_players.py`

## License

MIT. See [LICENSE](./LICENSE).
