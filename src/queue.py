# Shanyun Gao 
 #queue.py

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def front(self):
        if len(self.items) != 0:
            return self.items[-1]
        else:
            return None

    def end(self):
        if len(self.items) != 0:
            return self.items[0]
        else:
            return None

    def size(self):
        return len(self.items)
