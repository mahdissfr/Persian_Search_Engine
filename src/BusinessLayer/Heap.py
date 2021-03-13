import math
import sys


class DocNode:
    def __init__(self, doc_id, index_list, similarity):
        self.docId = doc_id
        self.indexList = index_list
        self.similarity = similarity

class MaxHeap:
    def __init__(self):
        self.heap = []
        self.heap.append(DocNode(-1, [], sys.float_info.max))
        # self.heap.append(sys.float_info.max)

    def getSize(self):
        return len(self.heap) - 1

    def parent(self, pos):
        return int(pos / 2)

    def leftChild(self, pos):
        return 2 * pos

    def rightChild(self, pos):
        return 2 * pos + 1

    def isLeaf(self, pos):
        if pos >= self.getSize() / 2 and pos <= self.getSize():
            return True
        return False

    def swap(self, fpos, spos):
        tmp = self.heap[fpos]
        self.heap[fpos] = self.heap[spos]
        self.heap[spos] = tmp

    def maxHeapify(self, pos):
        if self.isLeaf(pos):
            return

        if self.heap[pos].similarity < self.heap[self.leftChild(pos)].similarity or self.heap[pos].similarity < \
                self.heap[self.rightChild(pos)].similarity:
            if self.heap[self.leftChild(pos)].similarity > self.heap[self.rightChild(pos)].similarity:
                self.swap(pos, self.leftChild(pos))
                self.maxHeapify(self.leftChild(pos))

            else:
                self.swap(pos, self.rightChild(pos))
                self.maxHeapify(self.rightChild(pos))

    def insert(self, DocNode):
        self.heap.append(DocNode)
        current = self.getSize()
        while self.heap[current].similarity > self.heap[self.parent(current)].similarity:
            self.swap(current, self.parent(current))
            current = self.parent(current)

    def extractMax(self):
        i = self.getSize()
        if i > 1:
            popped = self.heap[1]
            self.heap[1] = self.heap.pop(i)
            self.maxHeapify(1)
            return popped
        elif i == 1:
            return self.heap.pop(i)
        else:
            return None


