import random

class RandomizedCollection:

    def __init__(self):
        self.map = {}
        self.__list_map = []
        self.start_pos = 0

    def insert(self, val: int) -> bool:
        if val in self.map:
            self.__list_map.append(val)
            self.map[val].append(len(self.__list_map) - 1)
            return False
        else:
            self.__list_map.append(val)
            self.map[val] = [len(self.__list_map) - 1]
            return True

    def remove(self, val: int) -> bool:
        if val in self.map:
            self.__list_map[self.map[val][0]] = None
            if self.map[val][0] == self.start_pos:
                self.start_pos += 1
                while self.start_pos < len(self.__list_map) and self.__list_map[self.start_pos] is None:
                    self.start_pos += 1
            self.map[val].pop(0)
            if len(self.map[val]) == 0:
                del self.map[val]

            return True
        else:
            return False
        
    def getRandom(self) -> int:
        i = random.randint(self.start_pos, len(self.__list_map)-1)
        while self.__list_map[i] is None:
            i = random.randint(self.start_pos, len(self.__list_map)-1)
        return self.__list_map[i]
        


# Your RandomizedCollection object will be instantiated and called as such:
# obj = RandomizedCollection()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()