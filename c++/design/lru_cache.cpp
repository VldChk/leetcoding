// LeetCode 146 - LRU Cache (Medium)
// https://leetcode.com/problems/lru-cache/
//
// Design a data structure that follows the constraints of a Least
// Recently Used (LRU) cache.
//
// Implement the LRUCache class:
//   - LRUCache(int capacity)        Initialize with positive capacity.
//   - int get(int key)              Return the value of the key if
//                                    present, else -1.
//   - void put(int key, int value)  Update or insert (key, value).
//                                    Evict the least recently used key
//                                    when over capacity.
//
// Both get and put must run in O(1) average time complexity.
//
// Solution idea:
//   Doubly-linked list of nodes ordered most-recently-used at the
//   front, plus an unordered_map<int, unique_ptr<Node>> for O(1)
//   key -> node lookup. Sentinel head_/tail_ nodes simplify boundary
//   handling: every real node always has non-null prev and next.
//   `move_to_front` is detach + insert_after_head and is the work
//   shared by `get` and the "key already exists" branch of `put`.
//   Ownership lives on the map (unique_ptr); the linked list stores
//   raw pointers for navigation, so erasing a key from the map
//   destroys the node and all pointers to it disappear together.

#include <cstddef>
#include <memory>
#include <unordered_map>

class LRUCache {
private:
    struct Node {
        int key = 0;
        int value = 0;

        Node* prev = nullptr;
        Node* next = nullptr;

        Node() = default;

        Node(int k, int v)
            : key(k), value(v) {}
    };

public:
    explicit LRUCache(int capacity)
        : capacity_(capacity > 0 ? static_cast<std::size_t>(capacity) : 0)
    {
        head_.next = &tail_;
        tail_.prev = &head_;
    }

    int get(int key) {
        auto it = nodes_.find(key);

        if (it == nodes_.end()) {
            return -1;
        }

        Node* node = it->second.get();
        move_to_front(node);

        return node->value;
    }

    void put(int key, int value) {
        if (capacity_ == 0) {
            return;
        }

        auto it = nodes_.find(key);

        if (it != nodes_.end()) {
            Node* node = it->second.get();
            node->value = value;
            move_to_front(node);
            return;
        }

        if (nodes_.size() == capacity_) {
            Node* victim = tail_.prev;
            detach(victim);
            nodes_.erase(victim->key);
        }

        auto new_node = std::make_unique<Node>(key, value);
        Node* raw_node = new_node.get();

        insert_after_head(raw_node);
        nodes_.emplace(key, std::move(new_node));
    }

private:
    std::size_t capacity_;

    Node head_;
    Node tail_;

    std::unordered_map<int, std::unique_ptr<Node>> nodes_;

    void detach(Node* node) {
        Node* before = node->prev;
        Node* after = node->next;

        before->next = after;
        after->prev = before;

        node->prev = nullptr;
        node->next = nullptr;
    }

    void insert_after_head(Node* node) {
        Node* old_first = head_.next;

        node->prev = &head_;
        node->next = old_first;
        
        head_.next = node;
        old_first->prev = node;
    }

    void move_to_front(Node* node) {
        detach(node);
        insert_after_head(node);
    }
};


// ----- local tests (not part of the LeetCode submission) -----
// Build and run:
//   g++ -std=c++17 lru_cache.cpp -o /tmp/lru && /tmp/lru
#include <cassert>
#include <iostream>

int main() {
    // LeetCode example 1
    LRUCache c(2);
    c.put(1, 1);                    // cache = {1=1}
    c.put(2, 2);                    // cache = {1=1, 2=2}
    assert(c.get(1) == 1);          // touches 1; LRU order now {2, 1}
    c.put(3, 3);                    // evicts 2; cache = {1=1, 3=3}
    assert(c.get(2) == -1);         // 2 was evicted
    c.put(4, 4);                    // evicts 1; cache = {3=3, 4=4}
    assert(c.get(1) == -1);         // 1 was evicted
    assert(c.get(3) == 3);
    assert(c.get(4) == 4);

    std::cout << "lru_cache.cpp: all tests passed" << std::endl;
    return 0;
}