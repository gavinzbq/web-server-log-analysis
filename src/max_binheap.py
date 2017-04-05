# Shanyun Gao    
# Binary Heap data structure: maxheap 

class max_BinHeap:
    def __init__(self):
        self.heaplist = [0]
        self.keylist = [None]
        self.currentsize = 0

    # build a binary heap with an input dict, based on dict values, with
    # maximum length constraint
    def build_heap(self, adict):
        i = len(adict) // 2
        self.currentsize = len(adict)
        self.heaplist = [0] + adict.values()
        self.keylist = [None] + adict.keys()
        while i > 0:
            self.percdown(i)
            i = i - 1

    def percdown(self,i):
        while (i * 2) <= self.currentsize:
            mc = self.maxchild(i)
            if self.heaplist[i] < self.heaplist[mc]:
                # process values
                tmpvalue = self.heaplist[i]
                self.heaplist[i] = self.heaplist[mc]
                self.heaplist[mc] = tmpvalue
                # process keys
                tmpkey = self.keylist[i]
                self.keylist[i] = self.keylist[mc]
                self.keylist[mc] = tmpkey
            i = mc
                
    def maxchild(self,i):
        if i * 2 + 1 > self.currentsize:
            return i * 2
        else:
            if self.heaplist[i * 2] > self.heaplist[i * 2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def perup(self,i):
        while i // 2 > 0:
            if self.heaplist[i] > self.heaplist[i//2]:
                # process values
                tmpvalue = self.heaplist[i // 2]
                self.heaplist[i // 2] = self.heaplist[i]
                self.heaplist[i] = tmpvalue
                # process keys
                tmpkey = self.keylist[(i // 2)]
                self.keylist[(i // 2)] = self.keylist[i]
                self.keylist[i] = tmpkey
            i = i // 2
 
    # insert a key value pair, dict[string] = value 
    def insert(self, string, value):
        self.heaplist.append(value)
        self.keylist.append(string)
        self.currentsize = self.currentsize + 1
        self.perup(self.currentsize)

    def del_max(self):
        retval = self.heaplist[1]
        self.heaplist[1] = self.heaplist[self.currentsize]
        retkey = self.keylist[1]
        self.keylist[1] = self.keylist[self.currentsize]
        self.currentsize = self.currentsize - 1
        self.heaplist.pop()
        self.keylist.pop()
        self.percdown(1)
        return (retkey, retval)
        
    def isempty(self):
        if currentsize == 0:
            return True
        else:
            return False

    def size(self):
        return self.currentsize
