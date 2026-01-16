class Node:
    def __init__(self, key, val):
        self.__val = val
        self.__key = key
        self._next = None
        self._prev = None
    
    @property
    def next(self):
        return self._next
    
    @next.setter
    def next(self, node):
        self._next = node

    @next.getter
    def next(self):
        return self._next

    @property
    def prev(self):
        return self._prev
    
    @prev.setter
    def prev(self, node):
        self._prev = node

    @prev.getter
    def prev(self):
        return self._prev
    
    @property
    def key(self):
        return self.__key
    
    @property
    def val(self):
        return self.__val


class LinkedList:
    def __init__(self):
        self.head = Node(-1, -1)
        self.tail = Node(-1, -1)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def add_node_next_to_head(self, node):
        prev_node = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = prev_node
        prev_node.prev = node
        
    def delete_node(self, node):
        next_node = node.next
        prev_node = node.prev
        next_node.prev = prev_node
        prev_node.next = next_node
        
    def delete_last_node(self):
        last_node = self.tail.prev
        if last_node is self.head:
            return
        else:
            self.delete_node(last_node)
        

class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.lru_list = LinkedList()
        self.capacity = capacity
        self.lru = {}
        

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        # print(self.lru_list)
        if key not in self.lru:
            return
        else:
            node = self.lru[key]
            self.lru_list.delete_node(node)
            self.lru_list.add_node_next_to_head(node)
            return node.val
        

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        # print(self.lru_list)
        new_node = Node(key, value)
        self.lru_list.add_node_next_to_head(new_node)
        if key in self.lru:
            old_node = self.lru[key]
            self.lru_list.delete_node(old_node)
            self.lru[key] = new_node
        else:
            if len(self.lru) >= self.capacity:
                last_node = self.lru_list.tail.prev
                del self.lru[last_node.key]
                self.lru_list.delete_node(last_node)
            self.lru[key] = new_node
        


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)