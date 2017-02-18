#!/usr/bin/env python3

from random import shuffle
from sys import stdin

def intersects0(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

class IntervalTree:
    class Node:
        def __init__(self, interval):
            self.interval = interval
            self.max = interval[1]
            self.left = None
            self.right = None

        def insert(root, interval):
            if not root:
                return IntervalTree.Node(interval)
            if interval[0] < root.interval[0]:
                root.left = IntervalTree.Node.insert(root.left, interval)
            else:
                root.right = IntervalTree.Node.insert(root.right, interval)
            if root.max < interval[1]:
                root.max = interval[1]
            return root

        def lookup(root, interval):
            if not root:
                return None
            if intersects0(root.interval, interval):
                return root.interval
            if root.left and root.left.max >= interval[0]:
                return IntervalTree.Node.lookup(root.left, interval)
            else:
                return IntervalTree.Node.lookup(root.right, interval)

        def inorder(root):
            if root:
                IntervalTree.Node.inorder(root.left)
                yield root
                IntervalTree.Node.inorder(root.right)

    def __init__(self, intervals):
        self.root = None
        intervals = intervals.copy()
        shuffle(intervals)
        for interval in intervals:
            self.root = IntervalTree.Node.insert(self.root, interval)

    def intervals(self):
        return map(lambda node: node.interval, IntervalTree.Node.inorder(self.root))

    def intersects_interval(self, interval):
        return IntervalTree.Node.lookup(self.root, interval) != None

    def intersects_interval_list(self, intervals):
        return any(self.intersects_interval(interval) for interval in intervals)

    def intersects(self, other):
        for interval in other.intervals():
            if self.intersects_interval(interval):
                return True
        return False

# --------------------------------------------------------------------------------------

class IntervalSet:
    def __init__(self, l):
        # self.first = [l[2 * i] for i in range(len(l) // 2)]
        # self.last = [l[2 * i + 1] for i in range(len(l) // 2)]
        # self.first.sort()
        # self.last.sort()
        self.intervals = [(l[2 * i], l[2 * i + 1]) for i in range(len(l) // 2)]

    def intersects(self, other):
        for i in self.intervals:
            for j in other.intervals:
                if intersects0(i, j):
                    return True
        return False

def intervals_of_list(l):
    return [(l[2 * i], l[2 * i + 1]) for i in range(len(l) // 2)]

def intervals_of_str(s):
    return intervals_of_list(list(map(int, s.split())))

if __name__ == '__main__':
    n, m = map(int, stdin.readline().split())
    genes = [IntervalTree(intervals_of_str(stdin.readline())) for _ in range(n)]
    reads = [intervals_of_str(stdin.readline()) for _ in range(m)]

    ans = [0] * n
    intersects = [[False] * n for _ in range(m)]

    for j in range(len(reads)):
        for i in range(len(genes)):
            intersects[j][i] = genes[i].intersects_interval_list(reads[j])
    # print(intersects)

    for j in range(len(reads)):
        try:
            i = intersects[j].index(True, 0)
            try:
                intersects[j].index(True, i + 1)
            except ValueError:
                ans[i] += 1
        except ValueError:
            pass
    print('\n'.join(map(str, ans)))
