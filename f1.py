#!/usr/bin/env python3

from sys import stdin

def intersects0(a, b):
    return a[0] <= b[1] and b[0] <= a[1]

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

n, m = map(int, stdin.readline().split())
genes = [IntervalSet(list(map(int, stdin.readline().split()))) for _ in range(n)]
reads = [IntervalSet(list(map(int, stdin.readline().split()))) for _ in range(m)]

ans = [0] * n
intersects = [[False] * n for _ in range(m)]

for j in range(len(reads)):
    for i in range(len(genes)):
        intersects[j][i] = genes[i].intersects(reads[j])
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
