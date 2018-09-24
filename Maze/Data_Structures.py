from collections import deque
from abc import ABC, abstractmethod


class DataStructure(ABC):
    """DataStructure is an abstract class that is the base class of Stack and Queue"""

    def __init__(self, list_):
        self.list = list_

    def size(self):
        return len(self.list)

    def peek(self):
        temp = self.list.remove()
        self.list.add(temp)
        return temp

    @abstractmethod
    def add(self, object_):
        pass

    @abstractmethod
    def remove(self):
        pass


class Stack(DataStructure):
    def __init__(self):
        super().__init__([])

    def add(self, object_):
        self.list.append(object_)

    def remove(self):
        return self.list.pop()


class Queue(DataStructure):
    def __init__(self):
        super().__init__(deque())

    def add(self, object_):
        self.list.append(object_)

    def remove(self):
        return self.list.popleft()
